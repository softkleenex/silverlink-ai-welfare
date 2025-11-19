# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SilverLink** is a Streamlit-based AI voice service that helps elderly Korean citizens discover and apply for welfare benefits they're eligible for. The application addresses the 30% welfare benefit non-application rate by providing an accessible, voice-first interface for seniors facing digital literacy challenges.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run the Streamlit app (opens at http://localhost:8501)
streamlit run app.py
```

### Environment Configuration
- Copy `.env.example` to `.env` and add your Gemini API key
- Required API key: `GEMINI_API_KEY` (get from https://aistudio.google.com/app/apikey)
- This single API key handles both STT and AI analysis via Gemini multimodal capabilities

## Architecture

### Single-File Design Philosophy
The entire application is contained in `app.py` (~576 lines) following a deliberate single-file architecture optimized for solo development and rapid iteration. This is intentional - do not split into modules unless there's a compelling reason.

### Core Data Flow

1. **Input Processing** (3 pathways):
   - Text input: Direct text → Gemini analysis
   - File upload: Audio file → Gemini File API → multimodal analysis
   - Real-time recording: Browser audio → temp file → Gemini File API

2. **AI Processing Pipeline**:
   - **Text input**: `create_prompt()` → Gemini text generation
   - **Audio input**: `create_audio_prompt()` → Gemini multimodal (STT + analysis in one call)
   - Both return structured JSON responses with greeting, benefits array, and encouragement

3. **Response Handling**:
   - `parse_and_display_response()`: Extracts JSON (handles ```json``` wrappers)
   - Displays structured UI with expandable benefit cards
   - Generates concatenated text for TTS
   - gTTS converts response to Korean audio

### Key Architectural Decisions

**Gemini-First Approach**: Uses Google Gemini 2.5 Pro for all AI operations. The multimodal capability allows audio files to be processed directly without separate STT service, consolidating the tech stack and reducing API complexity.

**JSON-Structured Prompts**: All Gemini prompts explicitly request JSON responses with defined schema:
```json
{
  "greeting": "...",
  "benefits": [{"name", "target", "amount", "description", "next_action", "documents", "contact"}],
  "encouragement": "..."
}
```
Audio prompts additionally include `"transcript"` field for displaying recognized speech.

**Welfare Data**: `welfare_data.json` contains 10 welfare benefit programs. The entire dataset is embedded in Gemini prompts (via `json.dumps()`) for context-aware matching. No database - benefits are statically loaded and cached via `@st.cache_data`.

**State Management**: Relies on Streamlit's session state and tab-based UI. Each tab (text/file/recording) operates independently. No complex state management needed due to simple request-response flow.

## Important Implementation Details

### Prompt Engineering
- Both text and audio prompts reference official Korean welfare resources (www.bokjiro.go.kr)
- Prompts instruct to recommend contacting local welfare centers (129) for uncertain cases
- Responses use formal Korean (존댓말) appropriate for elderly users
- The `create_prompt()` and `create_audio_prompt()` functions are the heart of AI behavior - modify these carefully

### Error Handling Pattern
All Gemini API calls follow this error handling pattern:
```python
try:
    # Gemini API call
except Exception as e:
    error_msg = str(e)
    if "API key" in error_msg:
        # API key error
    elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
        # Quota error
    # ... specific error types
    else:
        # Generic error
    st.info("💡 Helpful recovery suggestion")
    st.stop()
```
Preserve this pattern when modifying API interactions - it provides user-friendly Korean error messages.

### Audio File Handling
- Audio uploads: Saved as `temp_audio.mp3`
- Recordings: Saved as `temp_recorded_audio.wav`
- Response audio: Saved as `response.mp3`
- Files are written to working directory (not cleaned up between runs - Streamlit reruns are stateless)
- Use `genai.upload_file(path)` for Gemini File API, not base64 encoding

### Mobile Responsiveness
Custom CSS in `st.markdown()` at app.py:184-286 provides:
- Responsive breakpoints: 768px (tablet), 480px (mobile)
- Touch optimization with `touch-action: manipulation`
- Large fonts (3rem desktop → 1.5rem mobile for titles)
- Large buttons (min-height: 60px for touch targets)

Do not remove or significantly modify this CSS without testing on mobile devices.

### Streamlit Configuration
`.streamlit/config.toml` sets:
- Theme colors (blue primary #1E88E5)
- Server config (headless mode, port 8501)

Page config in app.py sets layout="wide" and custom page title/icon.

## Modifying Welfare Benefits

To add/modify benefits in `welfare_data.json`, ensure each entry has:
```json
{
  "id": unique_number,
  "name": "benefit name",
  "target": "eligibility criteria",
  "benefits": "description of benefits",
  "amount": "monetary value",
  "how_to_apply": "application process",
  "documents": ["required", "documents"],
  "contact": "contact info with phone number"
}
```

The AI will automatically use new benefits in recommendations - no prompt changes needed unless you want to emphasize specific programs.

## Testing Approach

Since this is a Streamlit app with no test suite, testing is manual:

1. **Text input test**: Use example scenarios from README.md (72-year-old living alone, low-income senior)
2. **Audio file test**: Upload a Korean audio file with age/situation description
3. **Real-time recording test**: Record via browser (requires HTTPS in production)
4. **Error scenarios**: Test with invalid API key, network disconnect, malformed audio

Always test all three input tabs after significant changes.

## Deployment Notes

The app is designed for Streamlit Cloud deployment (see DEPLOYMENT.md). Key considerations:

- Environment variables via Streamlit secrets management
- Real-time recording requires HTTPS (Streamlit Cloud provides this)
- No persistent storage needed - all data in JSON file
- Audio files are temporary and not persisted between sessions

## Korean Language Considerations

All user-facing text is in Korean. When modifying strings:
- Use formal speech (존댓말) for all AI responses
- Age-appropriate vocabulary (avoid technical jargon)
- Clear, simple sentence structure
- Maintain warm, encouraging tone (following the "복지 도우미" persona)

TTS uses gTTS with `lang='ko'` and `slow=False`. For elderly users, consider `slow=True` if feedback indicates speech is too fast.
