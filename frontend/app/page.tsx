"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import Orb from "@/components/orb";
import { v4 as uuidv4 } from "uuid";
import { BrainClient } from "@/utils/brain_client";

export default function Home() {
  const [isActive, setIsActive] = useState(false);
  const [isTalking, setIsTalking] = useState(false); // AI is talking
  const [volume, setVolume] = useState(0); // For visualization
  const [status, setStatus] = useState("Click to Start");

  const brainRef = useRef<BrainClient | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const recognitionRef = useRef<any>(null); // SpeechRecognition
  const audioQueueRef = useRef<string[]>([]); // Queue for audio chunks
  const isPlayingRef = useRef(false);

  // Initialize Audio Context & WebSocket
  const startSession = async () => {
    try {
      // 1. Audio Context
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();

      // 2. Brain Client
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const brain = new BrainClient(apiUrl);

      brain.connectWebSocket(
        (data) => { // onMessage
          if (data.type === "text") {
            setStatus(data.content); // Show text subtitle
          } else if (data.type === "audio") {
            // Queue audio
            audioQueueRef.current.push(data.data);
            playNextAudioChunk();
          }
        },
        () => { // onOpen
          setStatus("Listening...");
          setIsActive(true);
        },
        () => { // onClose
          setStatus("Disconnected");
          setIsActive(false);
        }
      );

      brainRef.current = brain;

      // 3. Speech Recognition
      if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onstart = () => {
          console.log("Recognition started");
        };

        recognition.onresult = (event: any) => {
          let interimTranscript = "";
          let finalTranscript = "";

          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript;
            } else {
              interimTranscript += event.results[i][0].transcript;
            }
          }

          // Interruption Logic: If user speaks, stop AI
          if (interimTranscript.length > 0 || finalTranscript.length > 0) {
            if (isTalking) {
              stopAiPlayback();
            }
            // Visualize user volume (mocked for now based on text length)
            setVolume(Math.min((interimTranscript.length + finalTranscript.length) * 0.05, 1));
          }

          if (finalTranscript) {
            console.log("Final:", finalTranscript);
            // Send to backend via BrainClient
            brain.sendWsText(finalTranscript);
            setVolume(0);
          }
        };

        recognition.onerror = (event: any) => {
          console.error("Speech error:", event.error);
        };

        recognition.start();
        recognitionRef.current = recognition;
      } else {
        setStatus("Speech Recognition not supported");
      }

    } catch (e) {
      console.error("Setup error:", e);
      setStatus("Error connecting");
    }
  };

  const stopAiPlayback = () => {
    // Clear queue
    audioQueueRef.current = [];
    isPlayingRef.current = false;
    setIsTalking(false);

    // Send interrupt signal
    brainRef.current?.interrupt();
  };

  const playNextAudioChunk = async () => {
    if (isPlayingRef.current || audioQueueRef.current.length === 0 || !audioContextRef.current) return;

    isPlayingRef.current = true;
    setIsTalking(true);

    const chunkBase64 = audioQueueRef.current.shift();
    if (!chunkBase64) return;

    try {
      // Decode Base64
      const binaryString = window.atob(chunkBase64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }

      // Decode Audio
      const audioBuffer = await audioContextRef.current.decodeAudioData(bytes.buffer);

      // Play
      const source = audioContextRef.current.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(audioContextRef.current.destination);

      // Visualization
      const analyser = audioContextRef.current.createAnalyser();
      source.connect(analyser);
      analyserRef.current = analyser;
      visualizeAudio();

      source.onended = () => {
        isPlayingRef.current = false;
        if (audioQueueRef.current.length > 0) {
          playNextAudioChunk();
        } else {
          setIsTalking(false);
          setVolume(0);
        }
      };

      source.start(0);
    } catch (e) {
      console.error("Audio playback error:", e);
      isPlayingRef.current = false;
      setIsTalking(false);
    }
  };

  const visualizeAudio = () => {
    if (!analyserRef.current || !isPlayingRef.current) return;

    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    analyserRef.current.getByteFrequencyData(dataArray);

    // Calculate average volume
    let sum = 0;
    for (let i = 0; i < dataArray.length; i++) {
      sum += dataArray[i];
    }
    const average = sum / dataArray.length;
    setVolume(average / 128); // Normalize 0-2ish

    requestAnimationFrame(visualizeAudio);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-black text-white overflow-hidden relative">

      {/* Orb Container */}
      <div className="w-full h-full absolute inset-0 flex items-center justify-center">
        <Orb isActive={isActive} isTalking={isTalking} volume={volume} />
      </div>

      {/* Status Text */}
      <div className="z-10 text-center pointer-events-none">
        <h1 className="text-2xl font-light tracking-widest opacity-50 mb-4 uppercase">
          {isActive ? "Connected" : "Digital Organism"}
        </h1>
        <p className="text-lg font-mono text-purple-300 animate-pulse">
          {status}
        </p>
      </div>

      {/* Start Button Overlay */}
      {!isActive && (
        <button
          onClick={startSession}
          className="absolute z-20 px-8 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full backdrop-blur-md transition-all text-sm tracking-wider uppercase"
        >
          Initialize Voice Link
        </button>
      )}

    </main>
  );
}
