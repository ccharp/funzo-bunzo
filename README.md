# Funzo-Bunzo
A Domain Specific Language hosted in the web! 

## Strategy and Assumptions
* Focus on backend first, i.e. create server (HTTP interface) and DSL interpreter (langueage features)
  * Might allow time for automated backend testing
  * If all front-end features are implemented sequentially as specified, work will be repeated/undone (features are no accumulative). Therefore, my plan is to see how far I get on the backend and implement frontend features as time allows.
* The backend shall be stateless. This aligns with the specified "declarative" nature of the DSL. All information and parameters required to execute a request will be present in that request. 
* Input parameters are passed as HTTP parameters
* For simplicity, any error encountered during parsing or execution of the DSL will cause the interpreter to abort execution. The server will respond with 400/418 and JSON blurb specifying the error. There are no partial executions. 

## Feature Priority
The backend is prioritized. If time allows, I will construct a rudimentary frontend as a proof-of-concept.
1. Language features
  1. Entrypoint, tasks, and subtasks `${subtask}`
  2. Input parameter `@{param}`
  3. Steps
    a. wait (maybe do this one last since it requires parallel execution)
    b. length  (do this at least, providing the scaffolding for other features save others for later if there's time)
    c. gt
    d. if 
  4. Implicit return (last statement executed)
  5. Debug stream
2. HTTP server
  1. Create single DSL execution endpoint
    a. Accept JSON and pass to interpreter
    b. Return result of execution or error
    c. Encode specific interpreter error in JSON 
3. Front-end
4. Brainstorming new features
   * 
   * Implementation order
