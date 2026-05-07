# ========= Tasks =========
- famil web scraping
  - kartik repo
  - galaxy faqs
- understand scientific workflows: galaxy

- hours tracker


# Questions
- how will agent interact with galaxy? find tools, construct workflow, ...
  - galaxy api, galaxy tool
  - galaxy tool list, documentation

# ========= Notes =========

- what agents will be used? - tbd
- what agent framework will be used? any decisions made on this?
  - langgraph

KeePassXC
~/KeePassXC/AppRun

### Galaxy
- web based data analysis platform

## Papers:
### MapCoder
  - agent framework for competitive programming
  - 4 agents with dynamic agent traversal
    - retrieval
    - planning
    - coding
    - debugging

### AgentCoder
  - code gen agent framework focused on improved test generation and lower token use
  - 3 agents
    - programmer
    - test designer
    - test executor
  - loop until correct answer

### CodeAgent
  - repo level code generation
  - 4 agent strategies
    - ReAct
    - Tool-Planning
    - OpenAIFun
    - Rule-based form
  - create CODEAGENTBENCH to test CodeAgent
  - use DuckDuckGo api for web search: https://api.duckduckgo.com/  
  - BM25 - documentation reading tool
  - treesitter for code symbol navigation

### Improved Bug Localization with AI Agents Leveraging Hypothesis and Dynamic Cognition
  - CogniGent - multiple agents
  - conduct hypothesis testing
  - 1. make hpothesis on root cause of bug
  - 2. causal reasoning to find starting points, explore dependent code
  - Click2Cause algorithm - depth-first traversal of call graph
      

### Benchmarks
  HumanEval
  MBPP - most basic program problems

### Web Scraping
    Selenium - framework to open and manipulate browser
    - start session
        driver = webdriver.Firefox() / webdriver.Chrome()
        add options for firefox:
            options = webdriver.FirefoxOptions()
            options.add_argument("-headless")
    - take actions
    - request info from browser
        title, current_url
    - wait
        implicit wait
            - driver.implicitly_wait(2)
            - wait this long for element
            - if element found before wait time, return
            - if timeout, error
        explicit wait
            - wait until explicit condition is met
            - if timeout, return error
    - find elements
        locate by: class, id, name, tag, link text
    - interact w elements
    - request element info
    - close session
        driver.quit()

# ========= days record =========

R 7 May
    - Galaxy forum scraping research
    - Attempted Selenium + BeautifulSoup scraper for help.galaxyproject.org
        - Issues: slow (sleep(2) waits), brittle DOM selectors, memory-intensive
    - Discovered forum runs Discourse software with public REST API
    - Key endpoints: /latest.json, /t/{slug}/{id}.json, /site.json, /about.json, /u/{username}.json
    - Discourse returns structured JSON: post_stream, topics, users, metadata
    - Next: replace Selenium with requests-based API crawler
        - pagination, batch fetching, retry/backoff, write to JSONL
        - analyze issue patterns for research validation
    - public endpoints:
        - `https://help.galaxyproject.org/latest.json` - topic list (paginated)
        - `https://help.galaxyproject.org/t/{slug}/{id}.json` - full topic with all posts
        - `https://help.galaxyproject.org/site.json` - categories, tags, site metadata
        - `https://help.galaxyproject.org/about.json` - site stats, moderators, version
        - `https://help.galaxyproject.org/u/{username}.json` - public user profile

W 6 May
    - convo w khairul about aim, new task
    - write email to techsupport asking for sudo access
        - sudo access granted
        - downloaded tmux, nvim, vscode
        - update sioyek exec
    - request lab key

T 5 May
    - Papers read:
    - AgentCoder: Multi-Agent Code Generation with Effective Testing and Self-optimisation 
    - CODEAGENT: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-level Coding Challenges
    - read bug localization paper
    - read up on benchmarks - HumanEval, MBPP, APPS, ...
    - galaxy: tools, workflows, scientific workflows
    - install ollama, run model
    - test out langchain, make minimal agent
    - make minimal agent
         define minimal task
         download ollama

M 4 May
    - onboarding
    - intro to projects, read up on agents, workflows
        - usegalaxy,  nextflow, snakemake
    - read MapCoder