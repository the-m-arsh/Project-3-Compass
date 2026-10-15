# Compass
 
Compass is an AI assistant that works on tasks for you using a real web browser, a sandbox
filesystem, web search, and Wikipedia. Give it a task and it keeps working until it's done,
checking its own work before it stops.
 
If your request is about starting something in a domain you're new to (a business, a hobby, a
career change), Compass recognizes this on its own and builds a structured **learning path**
instead of a plain answer. If your request is broad, it asks which direction you mean before it
starts researching.
 
Every learning path has the same seven sections, in this order:
 
1. Domain overview
2. Key regulations or requirements
3. Key players
4. Skills you'll need
5. Prioritized resources
6. Common beginner mistakes
7. Estimated timeline
Compass cites a source for every fact, says so when it can't find one, and adds a disclaimer
to anything legal, financial, or regulatory. The finished learning path appears in the chat and
is also saved as a file in the `sandbox/` folder.
 
## How it works
 
Two AI models play different roles:
 
- **The worker** (Google Gemini) does the task: browsing, searching, reading, and writing files.
- **The evaluator** (OpenAI GPT) checks the worker's answer and either accepts it, sends it back
  with feedback for another attempt (up to 3), or flags that it needs input from you.
Safeguards built in:
 
- When Compass hits something only a human can do (logging in, a CAPTCHA, two-factor
  authentication), it pauses and asks you to do it in the browser window, then continues once
  you approve.
- Email addresses and credit card numbers are redacted from what the model sees.
- A hard cap on model calls per task prevents runaway loops.
- If a tool fails, the error goes back to the model so it can try another approach instead of
  crashing the run.
## Using the app
 
1. Type your first request in the message box and click **Go!**
2. Compass works on it while a **Plan** panel on the right shows its live to-do list.
3. After Compass responds, the message box is disabled and a **reply box** appears. Use it for
   everything else in that conversation, such as answering a question or giving more
   instructions.
4. Click **Reset** to end the conversation and start a fresh one.
## Setup
 
### Requirements
 
- [Python](https://www.python.org/downloads/) 3.12 or newer
- [uv](https://docs.astral.sh/uv/) for managing dependencies
- [Node.js](https://nodejs.org/), because the browser and filesystem tools run as local MCP
  servers launched with `npx`
- API keys for [OpenAI](https://platform.openai.com/), [Google Gemini](https://aistudio.google.com/),
  and [Serper](https://serper.dev/) (used for web search)
### Install and run
 
```bash
git clone https://github.com/YOUR-USERNAME/compass.git
cd compass
uv sync
```
 
Create a file named `.env` in the project folder with your keys:
 
```
OPENAI_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
SERPER_API_KEY=your-key-here
```
 
Then start the app:
 
```bash
uv run app.py
```
 
The app opens in your browser. When a task needs the browser tool, a separate browser window
opens too. That's Compass at work, not a bug.
 
> Never commit your `.env` file. It's listed in `.gitignore` so Git skips it by default.
 
## Project structure
 
| File | What it does |
| --- | --- |
| `app.py` | The Gradio web interface |
| `compass.py` | The worker and evaluator loop, plus the agent's system prompt |
| `compass_tools.py` | The tools Compass can use: search, Wikipedia, browser, filesystem, and the human-help request |
| `styles.py` | The app's dark theme and orange accent styling |
 
## Customizing
 
- **Change the worker or evaluator model:** edit the model names in `Compass.setup()` in
  `compass.py`. The worker uses LangChain's `provider:model` format, so switching providers is
  a one-line change.
- **Change how Compass behaves:** the system prompt, including the learning-path rules, is the
  `WORKER_PROMPT` string in `compass.py`.
- **Add tools:** add them to `get_all_tools()` in `compass_tools.py`.
## Acknowledgments
 
Compass started from the Sidekick project in Ed Donner's *AI Engineer Agentic Track: The
Complete Agent & MCP Course* and has been extended from there.
