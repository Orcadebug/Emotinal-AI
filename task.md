# Task: Implement Conversational Identity

- [x] Create Implementation Plan <!-- id: 0 -->
- [x] Modify Database Schema <!-- id: 1 -->
    - [x] Add `sessions` table in `backend/brain.py`
- [x] Implement Session Logic in `backend/brain.py` <!-- id: 2 -->
    - [x] Implement `get_session` and `create_session`
    - [x] Implement `update_session_activity`
    - [x] Implement identity resolution state machine in `process_message`
- [x] Verify Changes <!-- id: 3 -->
    - [x] Test new session creation
    - [x] Test identity prompt ("Who is this?")
    - [x] Test identity resolution
    - [x] Test 4-hour timeout (simulated)
- [x] Update Documentation <!-- id: 4 -->
    - [x] Update `API_USAGE_GUIDE.md` to reflect the new conversational flow
