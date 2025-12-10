export class BrainClient {
    private apiUrl: string;
    private wsUrl: string;
    private ws: WebSocket | null = null;
    private onMessageCallback: ((data: any) => void) | null = null;

    constructor(baseUrl: string) {
        // Ensure no trailing slash
        const cleanUrl = baseUrl.replace(/\/$/, "");
        this.apiUrl = cleanUrl;
        // Convert http/https to ws/wss
        this.wsUrl = cleanUrl.replace(/^http/, "ws") + "/ws/chat";
    }

    /**
     * Send a text message via REST API
     */
    async sendText(userId: string, message: string): Promise<{ response: string; mood: string }> {
        try {
            const res = await fetch(`${this.apiUrl}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, message }),
            });
            if (!res.ok) throw new Error("Failed to send message");
            return await res.json();
        } catch (e) {
            console.error("BrainClient Error:", e);
            throw e;
        }
    }

    /**
     * Connect to WebSocket for real-time voice/text
     */
    connectWebSocket(onMessage: (data: any) => void, onOpen?: () => void, onClose?: () => void) {
        if (this.ws) this.ws.close();

        this.ws = new WebSocket(this.wsUrl);
        this.onMessageCallback = onMessage;

        this.ws.onopen = () => {
            console.log("Connected to Brain via WebSocket");
            if (onOpen) onOpen();
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (this.onMessageCallback) this.onMessageCallback(data);
        };

        this.ws.onclose = () => {
            console.log("Disconnected from Brain");
            if (onClose) onClose();
        };

        this.ws.onerror = (err) => {
            console.error("WebSocket Error:", err);
        };
    }

    /**
     * Send text via WebSocket
     */
    sendWsText(content: string) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ type: "text", content }));
        } else {
            console.warn("WebSocket not connected");
        }
    }

    /**
     * Interrupt current generation
     */
    interrupt() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ type: "interrupt" }));
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
}
