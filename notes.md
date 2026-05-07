# Tasks
- [ ] Understand scientific workflows: Galaxy
- [ ] Hours tracker

---

# Questions

- How will agent interact with Galaxy? Find tools, construct workflow, ...
  - Galaxy API
  - Galaxy tool list & documentation
- What agents will be used? **TBD**
- What agent framework will be used?
  - **LangGraph** (decision made)

---

# Notes

## Setup
- KeePassXC: `~/KeePassXC/AppRun`

## Galaxy
- Web-based data analysis platform

## Papers & Frameworks

### MapCoder
- Agent framework for competitive programming
- **4 agents** with dynamic agent traversal:
  - Retrieval
  - Planning
  - Coding
  - Debugging

### AgentCoder
- Code generation agent framework
- Focus: improved test generation, lower token use
- **3 agents**:
  - Programmer
  - Test designer
  - Test executor
- Loop until correct answer

### CodeAgent
- Repo-level code generation
- **4 agent strategies**:
  - ReAct
  - Tool-Planning
  - OpenAIFun
  - Rule-based form
- Created **CODEAGENTBENCH** for testing
- Tools:
  - DuckDuckGo API for web search: https://api.duckduckgo.com/
  - BM25 for documentation reading
  - TreeSitter for code symbol navigation

### Improved Bug Localization with AI Agents Leveraging Hypothesis and Dynamic Cognition
- **CogniGent** - multiple agents with hypothesis testing
- Process:
  1. Make hypothesis on root cause of bug
  2. Causal reasoning to find starting points
  3. Explore dependent code
- **Click2Cause algorithm** - depth-first traversal of call graph

### Benchmarks
- HumanEval
- MBPP (Most Basic Program Problems)

## Web Scraping

### Selenium Framework
- Open and manipulate browser

**Start session**:
```python
driver = webdriver.Firefox()  # or webdriver.Chrome()
options = webdriver.FirefoxOptions()
options.add_argument("-headless")
```

**Waiting strategies**:
- **Implicit wait**: Wait for element across all find operations
  ```python
  driver.implicitly_wait(2)
  ```
- **Explicit wait**: Wait until specific condition met
  ```python
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id")))
  ```

**Common operations**:
- Find elements: by class, ID, name, tag, link text
- Interact with elements
- Request element info
- Get page info: `title`, `current_url`
- Close session: `driver.quit()`

---

# Public Discourse API Endpoints

| Endpoint | Purpose |
|---|---|
| `/latest.json` | Topic list (paginated) |
| `/t/{slug}/{id}.json` | Full topic with all posts |
| `/site.json` | Categories, tags, site metadata |
| `/about.json` | Site stats, moderators, version |
| `/u/{username}.json` | Public user profile |

**Base URL**: `https://help.galaxyproject.org`

---

# Daily Record

## Thursday, 7 May
- Galaxy forum scraping research
- Familiarized with web scraping
  - reviewed kartik repo
  - reviewed galaxy forum
- Attempted Selenium + BeautifulSoup scraper for help.galaxyproject.org
  - **Issues**: slow (sleep(2) waits), brittle DOM selectors, memory-intensive
- **Discovery**: Forum runs Discourse software with public REST API
- **Key endpoints identified** (see table above)
- Discourse returns structured JSON: post_stream, topics, users, metadata
- **Next steps**:
  - Replace Selenium with requests-based API crawler
  - Implement pagination, batch fetching, retry/backoff
  - Write data to JSONL
  - Analyze issue patterns for research validation
- wrote script to save galaxy forum data using Dicourse api

## Wednesday, 6 May
- Conversation with Khairul about aim & new task
- Email to techsupport requesting sudo access → **Granted**
- Downloaded: tmux, nvim, vscode
- Updated sioyek executable
- Requested lab key

## Tuesday, 5 May
- Papers read:
  - AgentCoder: Multi-Agent Code Generation with Effective Testing and Self-optimisation
  - CODEAGENT: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-level Coding Challenges
  - Bug localization paper
- Galaxy research: tools, workflows, scientific workflows
- Benchmark research: HumanEval, MBPP, APPS
- Installed Ollama & tested model
- Tested LangChain & built minimal agent
- Task definition & minimal agent setup

## Monday, 4 May
- Onboarding
- Project intro & agent/workflow research
  - UseGalaxy, Nextflow, Snakemake
- Read MapCoder paper