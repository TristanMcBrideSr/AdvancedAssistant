
---

# Advanced HoloAssistant (Everything within the basic version with the addition of Voice(STT andTTS))

A multi-provider AI assistant powered by **HoloAI** with support for **OpenAI, Google Gemini, Anthropic Claude, xAI Grok, and Groq**.
This project includes memory handling, provider switching, skill/action integration, and a conversational loop.

---

## 🚀 Features

* Unified interface for multiple AI providers
* Easy `.env` configuration for API keys and models
* Conversational memory with turn limits
* Extendable skills and actions via `SkillGraph`
* Extendable tools via `SkillGraph`
* Supports text, vision, and file inputs
* Tunable **optional parameters** for advanced customization

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

Required packages:

* `HoloAI`

---

## ⚙️ Environment Setup

Create a `.env` file in your project root:

```ini
# Default provider (openai, google, groq, anthropic, xai)
PROVIDER=openai  

# API keys (set only the ones you need)
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
XAI_API_KEY=your_xai_api_key
```

Optional overrides for models:

```ini
OPENAI_RESPONSE_MODEL=gpt-4.1
OPENAI_VISION_MODEL=gpt-4.1
...
```

---

## 🖥️ Usage

```bash
python AdvancedAssistant.py
```

Example:

```
You: Hello
Holo Assistant: Hi! How can I help you today?
```

---

## 🧩 Supported Prompts

### Images

Formats: `png`, `jpg`, `gif`

```
What is in this image? C:\images\dog.png
```

### Files

Formats: `txt`, `pdf`, `docx`

```
Tell me about this file C:\docs\report.txt
```

### Mixed Inputs

```
Tell me about these C:\images\photo.png, C:\docs\notes.txt
```

---

## ⚡ Skills and Actions

The assistant integrates with **SkillGraph**:

* `getAgentCapabilities()` → available skills
* `getAgentActions()` → executable actions

Both are optional and passed into `HoloCompletion`.

---

## 🧠 Memory

* Stores recent conversation history
* Default limit: **10 turns**
* Oldest messages are discarded once the limit is exceeded

---

## 🎛️ Optional Parameters (Advanced)

You can customize the assistant’s behavior by adjusting the following optional parameters in `HoloCompletion`:

* **`skills`** *(default: None)*
  Skills from `SkillGraph` to expand assistant’s knowledge.

* **`actions`** *(default: None)*
  Actions the assistant can trigger from `SkillGraph`.

* **`tools`** *(default: None)*  
  A list of external functions the assistant can call.  
  - These are traditional **tool/function calls** (not built-in skills).  
  - You are responsible for handling the function execution yourself.  
  - For example, you might expose a calculator, database query, or API call.  

  👉 See [FunctionCalling](https://github.com/TristanMcBrideSr/FunctionCalling) for a complete example of how to define and use tools.


* **`tokens`** *(default: 4096)*
  Maximum tokens allowed in a response. Increase for long outputs.

* **`budget`** *(default: None)*
  Reserved tokens for planning/thinking. Must be smaller than `tokens`.

* **`effort`** *(default: auto)*
  Effort level for reasoning (`low`, `medium`, `high`, or `auto`).

* **`creativity`** *(default: 0.2)*
  Equivalent to temperature.

  * `0.0` → deterministic
  * `1.0` → highly creative

* **`files`** *(default: None)*
  Pass file paths (images, PDFs, docs) directly. Example:

  ```python
  files=[r"C:\images\cat.png", r"C:\docs\notes.txt"]
  ```

* **`colloect`** *(default: 10)*
  For animations/videos: collects the first, last, and every *n*-th frame.

* **`verbose`** *(default: False)*
  Returns full raw response structure (not just text).

---

## 👨‍💻 For Developers

* **Beginners**: Configure `.env`, run `HoloAssistant.py`, and start chatting.
* **Experienced Devs**: Override models, inject custom skills/actions, or extend `HoloCompletion()` with tools/APIs.

---

## License

This project is licensed under the [Apache License, Version 2.0](LICENSE).
Copyright 2025 Tristan McBride Sr.

You may use, modify, and distribute this software under the terms of the license.
Please just give credit to the original authors.

If you like this project, consider supporting it by starring the repository or contributing improvements!

---

## Acknowledgements

Project by:
- Tristan McBride Sr.
- Sybil
