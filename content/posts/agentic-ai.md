+++
title = "Agentic AI"
description = "Stripping an AI agent down to its essential mechanism"
tags = [
    "agents",
    "llm",
]
date = "2026-06-17"
categories = [
    "concept",
]
menu = "main"
parent = "notebook"
+++

What are "agents" ? Instead of duck-testing this, let's ask what mechanically makes a program an agent ? (rather than a function call with good marketing)

## 1. What is agency ?
The [Cambridge dictionary](https://dictionary.cambridge.org/dictionary/english/agency) says: *the ability to take action or to choose what action to take.*

## 2. Where does the agency come from in agentic AI?
An LLM, on its own, is a function mapping a text to a text. You give it a prompt, it returns one completion, and then it is done. It cannot check the weather. It cannot notice it was wrong and try again. So where does the *agency* come from?

Not from the model. From the loop around the model.

## 3. Stripping it down
What is the smallest version of an agent that still contains its essential algorithmic content?

Throw out everything that is add-on and not a mechanism : frameworks, planners, memory stores, vector databases, multi-agent "swarms." None of those are the agent. They are complexity we can add little by little, only if the bare loop demands it. (It usually doesn't)

What's left when you delete all of it:

1. a **model** that, given the accumulated state, proposes the *next action*,
2. a set of **tools** the action can name,
3. an **executor** that runs the named tool and gets a result,
4. a **loop** that feeds the result back and asks again until the model says *stop*.

That's it.

In pseudocode we can summarize it like this:
```python
state = initial_observation()
goal = user_goal

while not done(state, goal):
    action = policy(state, goal)      # decide what to do
    observation = environment.step(action)  # act, get result
    state = update(state, action, observation)

return final_answer(state)
```

### 3.1. Let's build the core

To focus on the loop we replace the LLM with a fake one. A hardcoded function that returns actions the way a real model would, but deterministically.

{{% details "Show the full code" %}}
```python
# tools are functions. the "agent" is not allowed to know how they work.

def add(a, b):       return int(a) + int(b)

def multiply(a, b):  return int(a) * int(b)

TOOLS = {
    "add": add,
    "multiply": multiply,
}

# model: state -> next action. a real LLM does this with weights, we fake it with a script.
# task: compute (3 + 4) * 5. it must act, read the result, then act again.
def fake_model(history):
    last = history[-1]

    if last["role"] == "user":
        return {
            "type": "tool",
            "name": "add",
            "args": {"a": 3, "b": 4},
        }

    if last["role"] == "tool" and last["name"] == "add":
        return {
            "type": "tool",
            "name": "multiply",
            "args": {"a": last["content"], "b": 5},
        }

    if last["role"] == "tool" and last["name"] == "multiply":
        return {
            "type": "final",
            "content": f"answer = {last['content']}",
        }

    return {
        "type": "final",
        "content": "failed",
    }

#  this is the agent.
def run(task, model, tools, max_steps=10):
    history = [{"role": "user", "content": task}]
    print(f"TASK: {task}\n")

    for step in range(1, max_steps + 1):
        print(f"--- loop {step} ---")

        action = model(history)
        print(f"  1. model decided: {action}")

        history.append({"role": "assistant", "content": action})

        if action["type"] == "final":
            print("  2. type is 'final' -> returning\n")
            return action["content"], history

        if action["type"] != "tool":
            raise ValueError(f"Unknown action type: {action['type']}")

        if action["name"] not in tools:
            raise ValueError(f"Unknown tool: {action['name']}")

        result = tools[action["name"]](**action["args"])

        print(f"  3. ran tool {action['name']}({action['args']}) -> {result}")

        history.append({
            "role": "tool",
            "name": action["name"],
            "content": result,
        })

        print(f"  4. appended result; history now has {len(history)} messages\n")

    raise RuntimeError("agent did not finish - it looped")


answer, history = run("compute (3 + 4) * 5", fake_model, TOOLS)
print(answer)

```
{{% /details %}}

> [!CAUTION]
> **Important.** As we can see, the model does **not** run the tool. The model emits a structured action. The agent runtime executes that action. This distinction is central.

### 3.2. Let's evaluate the core

```shell

TASK: compute (3 + 4) * 5

--- loop 1 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': 3, 'b': 4}}
  3. ran tool add({'a': 3, 'b': 4}) -> 7
  4. appended result; history now has 3 messages

--- loop 2 ---
  1. model decided: {'type': 'tool', 'name': 'multiply', 'args': {'a': 7, 'b': 5}}
  3. ran tool multiply({'a': 7, 'b': 5}) -> 35
  4. appended result; history now has 5 messages

--- loop 3 ---
  1. model decided: {'type': 'final', 'content': 'answer = 35'}
  2. type is 'final' -> returning

answer = 35

```
In `loop 1` the model asks for `add(3, 4)`, the code runs it and appends `7` to history. In `loop 2` the model comes back with `multiply(7, 5)` and that `7` is the result it just observed, not something it knew up front. The second action depended on the observed result of the first. act, observe, act again on what you observed, this chain is the entire difference between an agent and a single model(prompt) call. Watch the message count climb and you are watching the agent "think". 

> [!DEFAULT]
> **Note.** Nothing here is "intelligent." `fake_model` is an `if` statement. And yet the loop already exhibits the defining behavior: tool use, feedback, termination. Hold onto that because this will tell you exactly which part is doing the work, and which part you've been overpaying for.

To push on the mock until it breaks, we can ask : What if the task were compute (10 + 2) * 9? What if the user asked for subtraction? What if the correct next tool depended on the wording of the task rather than the previous tool name?

Of course, fake_model will misfire because it is a fixed script. It does not understand the task. It does not parse the user request. It simply says: after the user message, call `add(3, 4)` and after an `add` result call multiply on `result` and `5` and then stop. This brittleness is the tell: it marks the exact spot where the intelligence needs to go. So in order to name what the hardcoded `if` is placeholder for we can postulate that a real LLM conditions on the whole accumulated `history` and decides the next move from context. The branch is a stand-in for reasoning. The loop around it does not see the difference.

> [!DEFAULT]
> **Note.** notice that `fake_model` never looks at the task. if we make `fake_model` parse the numbers out of the task string we would just be making a little calculator. "variable args from any task" is the LLM's job. 

### 3.3. Let's replace the fake model with a real one

{{% details "Show the full code" %}}
```python
# tools are functions. the "agent" is not allowed to know how they work.

def add(a, b):       return int(a) + int(b)
def multiply(a, b):  return int(a) * int(b)

TOOLS = {"add": add, "multiply": multiply}

## REAL MODEL
import ollama

LLM="qwen3-vl:30b" # any model is fine, i just had this one already pulled (just make sure the model has tool calling capability)

def real_model(history):
        response = ollama.chat( 
            model=LLM,
            messages=history,
            tools=list(TOOLS.values()),
            options={"temperature": 0}, 
        )
        msg =  response["message"]
        if msg.tool_calls:
            call = msg.tool_calls[0]
            return {"type": "tool", "name": call.function.name, "args": call.function.arguments,
                    "content": msg.content or "", "tool_calls": msg.tool_calls}

        return {"type": "final", "content": response["message"]["content"]}

#  this is the agent.
def run(task, model, tools, max_steps=10):
    history = [ 
        {"role": "user", "content": task}
        ]
    print(f"TASK: {task}\n")

    for step in range(1, max_steps + 1):
        print(f"--- loop {step} ---")
        # 1. ask the model what to do, given everything so far
        action = model(history)
        print(f"  1. model decided: {action}")
        
        # 2. is it a final answer? then we're done
        if action["type"] == "final":
            print("  2. type is 'final' -> returning\n")
            return action["content"], history

        history.append({"role": "assistant", "content": action.get("content", ""),
                        "tool_calls": action["tool_calls"]})

        # 3. it is a tool request ? then the runtime executes the tool
        name = action["name"]
        args = action["args"]
        if name not in tools:
            result = f"unknown tool: {name}"
        else:
            result = tools[name](**args)    

        print(f"  3. ran tool {name}({args}) -> {result}")
        # 4. append the result to history, then loop back to step 1
        history.append({"role": "tool", "name": name, "content": str(result)})
        print(f"  4. appended result; history now has {len(history)} messages\n")

    raise RuntimeError("agent did not finish — it looped")

if __name__ == "__main__":
    answer, _ = run("compute (2 + 4) * 5", real_model, TOOLS)
    print(answer)

```
{{% /details %}}

and this was the result of the first run:

```shell
TASK: compute (2 + 4) * 5

--- loop 1 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': '', 'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': '2', 'b': '4'}))]}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 3 messages

--- loop 2 ---
  1. model decided: {'type': 'tool', 'name': 'multiply', 'args': {'a': '6', 'b': '5'}, 'content': '', 'tool_calls': [ToolCall(function=Function(name='multiply', arguments={'a': '6', 'b': '5'}))]}
  3. ran tool multiply({'a': '6', 'b': '5'}) -> 30
  4. appended result; history now has 5 messages

--- loop 3 ---
  1. model decided: {'type': 'final', 'content': 'The computation of (2 + 4) * 5 is completed as follows:\n\n1. First, compute $2 + 4 = 6$ using the `add` function.\n2. Then, multiply the result by 5: $6 \\times 5 = 30$ using the `multiply` function.\n\nFinal answer: **30**'}
  2. type is 'final' -> returning

The computation of (2 + 4) * 5 is completed as follows:

1. First, compute $2 + 4 = 6$ using the `add` function.
2. Then, multiply the result by 5: $6 \times 5 = 30$ using the `multiply` function.

Final answer: **30**

```
> [!CAUTION]
> **Caution.** The agent works fine. But we got lucky here because the model is a reasoning model. See if you can spot why !

## 4. Experiments on the minimal agent
> [!DEFAULT]
> **Now that we have a minimal messy agent let's break it even more through a series of experiments.**

### 4.1. Experiment : Break the loop by not updating the action state
Let's omit the `"tool_calls": action["tool_calls"]` part and see what happens.

```shell
TASK: compute (2 + 4) * 5

--- loop 1 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': ''}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 3 messages

--- loop 2 ---
  1. model decided: {'type': 'tool', 'name': 'multiply', 'args': {'a': '6', 'b': '5'}, 'content': ''}
  3. ran tool multiply({'a': '6', 'b': '5'}) -> 30
  4. appended result; history now has 5 messages

--- loop 3 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': ''}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 7 messages

--- loop 4 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': ''}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 9 messages

--- loop 5 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': ''}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 11 messages

--- loop 6 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': ''}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 13 messages

--- loop 7 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': ''}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 15 messages

--- loop 8 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': ''}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 17 messages

--- loop 9 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': 'Which would result in 6 and then 30. So the final answer is 30.\n</think>'}
  3. ran tool add({'a': '2', 'b': '4'}) -> 6
  4. appended result; history now has 19 messages

--- loop 10 ---
  1. model decided: {'type': 'final', 'content': 'The calculation proceeds as follows:\n\n1. First, compute the addition inside the parentheses:  \n   $ 2 + 4 = 6 $  \n   This is done using the `add` function with inputs `"2"` and `"4"`, resulting in `"6"`.\n\n2. Next, multiply the result by 5:  \n   $ 6 \\times 5 = 30 $  \n   This is done using the `multiply` function with inputs `"6"` and `"5"`, resulting in `"30"`.\n\n**Final Answer:**  \n30'}
  2. type is 'final' -> returning

The calculation proceeds as follows:

1. First, compute the addition inside the parentheses:  
   $ 2 + 4 = 6 $  
   This is done using the `add` function with inputs `"2"` and `"4"`, resulting in `"6"`.

2. Next, multiply the result by 5:  
   $ 6 \times 5 = 30 $  
   This is done using the `multiply` function with inputs `"6"` and `"5"`, resulting in `"30"`.

**Final Answer:**  
30

```
As we can see from the log, Loop 2 already had the answer. But the model did not decide to stop. It only emitted final at loop 10.

- Our representation of history is not good enough: on every tool call we append `{"role": "assistant", "content": ""}` and not the tool call itself. The model's own actions never make it back into the history. The loop didn't fail. Our representation of history did.
- Stopping is a design problem we own: a real model does not reliably know when it is done. Producing the answer and deciding to stop are two different acts, and the second one is not guaranteed.

### 4.2. Experiment : Change the tools 
Let's modify the tools with:

```python
def add(a, b):       return a + b
def multiply(a, b):  return a * b
```
In the experiments I ran, the model seemed to choke on the false result and had a hard time getting to the multiply step.

{{% details "Example of qwen's answer" %}}
```shell
TASK: compute (2 + 4) * 5

--- loop 1 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 'content': '', 'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': '2', 'b': '4'})), ToolCall(function=Function(name='multiply', arguments={'a': '6', 'b': '5'}))]}
  3. ran tool add({'a': '2', 'b': '4'}) -> 24
  4. appended result; history now has 3 messages

--- loop 2 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 
  'content': 'But then the user\'s final answer was 24. 
  Wait, that\'s conflicting because (2+4)=6 multiplied by 5 is 30, not 24. So either there\'s a mistake in the tool calls or the result.
  Wait, maybe I need to check again. Let me redo the calculation: (2 + 4) * 5 = 6 * 5 = 30. But the user\'s example shows the tools returning 24. Wait, perhaps there was an error in the problem statement? Or maybe a typo.
  Wait, no. The user says "compute (2 + 4) * 5" but then the tool response after adding and multiplying gives 24. That doesn\'t add up. Maybe it\'s a mistake in the example. But according to the tools provided, the correct steps would be 6*5=30.
  Wait, looking at the user input again: They asked to compute (2 + 4) *5. Then the assistant called add(2,4), got 6, then multiply(6,5). But when they say "tool response" is 24, which would be incorrect. However, in the problem statement, maybe there\'s a different function or miscalculation.
  Wait, no. The user shows that after the two tool calls, the answer was 24. Wait, but how? (6 *5) is 30. So perhaps there\'s an error here. But according to the given problem setup, I need to follow what was done. Wait, maybe in the actual scenario, the multiply function might not be correctly called.
  Wait, let me check again: The user provides a tool for add and multiply. They used add with 2 and 4 (resulting in 6), then multiply with 6 and 5, which should give 30. However, the user says "compute (2 +4)*5" and the tools return 24. Wait, that\'s not possible unless there was a typo.
  Wait, perhaps I\'m missing something here. Let me check:\n\nIn the tool response section of the user input, it shows the final answer as 24. But according to the math, (2+4)*5=30. So either there is a mistake in the problem setup or perhaps the multiply function was called with different numbers.\n\nWait, but in the given example here, after making those two tool calls, why would it be 24? Maybe the user intended something else. But according to the tools provided, if you add 2 and 4 (6) then multiply by 5 gives 30, which is correct.\n\nHowever, looking at the assistant\'s answer in the problem statement: The user input shows that after tool responses, it says "24". So maybe there\'s a mistake here. But as an AI, I need to follow what\'s given. Wait, but perhaps the example was intended to be (2 + 4) * 3 which would be 18 or something else. 
  Hmm.
  Alternatively, maybe in their tool responses, they used different numbers. For instance, if the multiply step was with 6 and 4, that would give 24. But the user asked for multiplying by 5. So this seems inconsistent.
  Wait, but perhaps it\'s a typo in the problem. Let me check again:\n\nThe original user instruction says: "compute (2 + 4) * 5"\n\nBut the tools call are add(2,4)=6 and multiply(6,5)=30. However, in the tool response after those calls, they say 24.\n\nSo this is a discrepancy. But as per the problem\'s given context, perhaps I should assume that maybe there was an error in how it was presented. However, according to the actual tools called, the correct answer would be 30. Unless there\'s another step or function involved.\n\nWait, looking back at the tool definitions: The functions take \'a\' and \'b\' as strings. So when we do multiply(6,5), that should return "30", which is then returned as the final answer. But in the user input example provided here, it shows:Then the user response says 24. But that doesn\'t make sense. Wait, unless there\'s a third tool call? Or perhaps the multiply function was supposed to be used differently.\n\nAlternatively, maybe the initial steps were done incorrectly. For example, if they multiplied first instead of adding parentheses first, but according to order of operations, (2 + 4) *5 would require addition first.
  Wait, I\'m confused because there\'s a discrepancy between the correct calculation and what was presented in the problem. But given that this is a test case for me as an AI assistant, perhaps it\'s intended that after adding 2+4 to get 6, multiplying by 5 gives 30, but somehow in the example, they say it\'s 24. 
  Wait, no.\n\nWait, looking again: The user wrote:\n\n"compute (2 + 4) * 5"\n\nThe assistant calls add(2,4), then multiply(6,5). Then the system returns 24. But mathematically, this is wrong. However, perhaps there\'s a mistake in the problem statement. Maybe it was supposed to be (2 + 3) * 4 = 20 or something else.
  Alternatively, maybe I\'m missing that in their tool definitions, multiply takes parameters as strings but the actual multiplication function isn\'t working correctly. But according to standard operations, there\'s no way multiplying 6 by 5 gives 24.
  Wait, perhaps it was supposed to be (2 * 4) + 5 or another order? No, the user specified parentheses first.
  Hmm. Given this inconsistency, but assuming that the example is as provided, I need to check what the problem wants me to do here.\n\nBut as per the current scenario: The assistant called two functions and then returned 24. But according to calculations, it should be 30. However, in reality, maybe there was a mistake and the intended problem was (2 + 4) * 4 = 24. Or perhaps multiplication by 5 but using wrong numbers.\n\nAlternatively, maybe the multiply function is supposed to do something else, but according to the tool definition it\'s straightforward multiplication.\n\nThis seems like an error in the example, but as per instructions, I need to proceed with this data.\n\nWait, the user\'s message shows that after the two tool calls (add(2,4), multiply(6,5)), the answer is 24. Which implies a mistake here. But for some reason, perhaps they intended a different multiplication step.\n\nAlternatively, maybe in their tools function, there was a typo and it\'s actually 30 but the example says 24 by accident.
  However, as I need to generate an appropriate response based on this scenario, given that the tool calls resulted in those steps leading to a wrong answer (as per math), but perhaps it\'s intentional for testing.
  Wait, no. The user\'s message shows:\n\nAfter the tool responses, they say "24". So maybe there was a mistake and the correct step should have been something else. For example, if the problem was (3 + 1) * 6 = 24. But that\'s not relevant here.
  Alternatively, perhaps in the multiply function call, it\'s multiply(4,5)=20 plus 4? Not sure.\n\nBut given the current information, I have to assume that either there is a typo in the problem statement or maybe the assistant made an error.
  Wait, but according to the user input, when they said "compute (2 + 4) *5", then tools were called:\n\nadd(2,4)=6\n\nmultiply(6,5)=30. But the final answer given was 24. So there\'s a discrepancy here.\n\nAs per the problem statement, I need to follow what is written. The user said that after those tool calls, the result was 24. Perhaps it\'s a test case where even though in reality it should be 30, but for some reason they want me to present it as 24.\n\nBut no—my job here is to figure out if I\'m supposed to correct this or explain why there\'s a discrepancy.\n\nWait, the user wrote:\n\n"compute (2 + 4) * 5"\n\nAnd then in their tool response example, after calling add(2,4) and multiply(6,5), it says "24".\n\nBut that is incorrect. So perhaps there was an error in the problem setup. However, as per instructions, I need to use the provided tools to compute.\n\nAssuming everything else is correct, then the answer should be 30. But according to what\'s written here, maybe the multiply function call had different parameters.\n\nWait, let me check again: The second tool call was multiply(a=6, b=5), which equals 30. So if the user says after those calls it returned 24, then something is wrong. However, perhaps there\'s a mistake in the problem description where maybe "multiply" function is defined differently or the parameters were swapped.\n\nBut given that the tools are standard functions as specified:\n\nadd(a,b) = a + b\n\nmultiply(a,b) = a * b\n\nThen (2+4)=6, 6*5=30. So the correct answer should be 30. But according to the user\'s message in this example, it says the final result was 24.\n\nTherefore, there must be an error somewhere. However, since I have to work within what\'s given, perhaps it\'s a mistake in their problem statement.\n\nBut as per instructions, the assistant needs to answer based on the tool calls and results. In this case, if after two tool calls of adding and multiplying correctly, but result was shown as 24 instead of 30, then maybe there is an error in the setup. However, given that the tools have been called correctly with add(2,4) and multiply(6,5), the answer should be 30.\n\nBut perhaps the user made a mistake in their example response. As part of my task here, I need to provide the correct calculation based on the tool definitions. So even if in some hypothetical scenario they said it\'s 24, according to math it\'s 30.\n\nWait, but looking back at how this was presented: The user has a problem where they provided the tools, then there are two tool calls (add and multiply), followed by the answer being 24. But that would be incorrect unless there\'s another factor.
  Alternatively, maybe the assistant made a mistake in using the correct parameters for the multiplication step. For example, if after adding 2+4=6, they multiplied it by 4 instead of 5: 6*4=24. That could happen due to a typo.
  But according to the tool response shown here:It\'s multiplying by 5, not 4. So it should be 30.\n\nHmm. This is confusing. Given that this appears to be a test case for the AI assistant where they have to follow tool calls and compute accordingly.\n\nWait, in the problem statement provided:\n\nThe user says "compute (2 + 4) * 5", then shows two tool calls: add(2,4) → 6; multiply(6,5) → ?\n\nAnd then the system response is 24. Which contradicts the math.\n\nBut perhaps there\'s an error in how this was presented to me. Maybe "multiply" function does something else here. But according to the tool definition:\n\n{"type": "function", "function": {"name": "multiply", "parameters": {"a": {"type": "string"}, "b": {"type": "string"}}}}\n\nSo it\'s standard multiplication.\n\nGiven that, I\'m forced to assume there was a typo in the problem statement. For example, perhaps (2 + 3) *4 = 20 or another combination gives 24.
  But since the question specifically says (2+4)*5=6*5=30, but the answer given is 24, it\'s likely an error.\n\nHowever, as per instructions, I\'m to provide a response based on this scenario. If the user presented that after the tool calls the result was 24, then perhaps there was a miscalculation in one of the steps.\n\nWait, let me re-express: The problem may have intended to ask (3 + 3) * 4 = 24, but wrote (2+4)*5. Alternatively, it\'s possible that in another context the multiply function could be doing something different, like addition or subtraction, but according to tools provided, it should be multiplication.
  Assuming everything is correct as per given functions and parameters:\n\nStep 1: add(2,4) → result = "6"\n\nStep 2: multiply("6", "5") → 30\n\nSo the final answer must be 30. The mention of 24 in the tool response seems to be a mistake.\n\nBut since this is given as part of the example for me to process, perhaps I should still output the correct answer based on the tools.
  Wait, no—the user is showing that after certain tool calls (as per their setup), the result was 24. But why?
  Perhaps in their case, the multiply function had a bug where it multiplies by b-1 or something else. For instance, if they used multiply(6,5) but actually returned 6*3=18? Not sure.
  Alternatively, maybe there\'s an error in how the tool responses are processed here.
  Wait, looking back at the exact input from the user:\n\nuser', 'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': '2', 'b': '4'})), ToolCall(function=Function(name='multiply', arguments={'a': '6', 'b': '5'})), ToolCall(function=Function(name='add', arguments={'a': '2', 'b': '4'})), ToolCall(function=Function(name='multiply', arguments={'a': '6', 'b': '5'})), ToolCall(function=Function(name='multiply', arguments={'a': '6', 'b': '5'}))]}
  3. ran tool add({'a': '2', 'b': '4'}) -> 24
  4. appended result; history now has 5 messages

--- loop 3 ---
  1. model decided: {'type': 'final', 'content': ''}
  2. type is 'final' -> returning


```
{{% /details %}}

Why doesn't the model get to the multiply step ? It could've just added '2' and '4', which would have resulted in '24' and then multiply by '5'. I suspect this behavior is due to the model being gated. It will not advance to step 2 until step 1 produces a result it believes. 
I kept running several times to see if it would reach the multiply step and it did indeed after several tries :

```shell
--- loop 7 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': '2', 'b': '4'}, 
  'content': 'Then, using the result (which is "6"), call multiply:The multiply function would return "30", which is the correct answer. 
  But the user\'s previous tool responses show 24, which is incorrect. 
  So perhaps the user made a mistake in the problem statement, but according to the given problem, the answer should be 30.\n</think>'}
  3. ran tool add({'a': '2', 'b': '4'}) -> 24
  4. appended result; history now has 15 messages

--- loop 8 ---
  1. model decided: {'type': 'tool', 'name': 'multiply', 'args': {'a': '6', 'b': '5'}, 'content': ''}
Traceback (most recent call last):
  File "agent-mock-model.py", line 102, in <module>
    answer, _ = run("compute (2 + 4) * 5", real_model, TOOLS)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "agent-mock-model.py", line 92, in run
    result = tools[name](**args)
             ^^^^^^^^^^^^^^^^^^^
  File "agent-mock-model.py", line 4, in multiply
    def multiply(a, b):  return a * b
                                ~~^~~
TypeError: can't multiply sequence by non-int of type 'str'
```

2 new experiments that come to my mind here: 
1. what happens when we change the temperature ? (this one is straightforward, wrap the code in a loop and run the code multiple times for different temperatures - in my case it kept looping, while sometimes thinking about how it should be 6 instead, and then reached the RuntimeError each time) 
2. what happens when we pick a non-reasoning model ?

### 4.3. Experiment : Pick a non-reasoning model 

```python
# pull an actual non-reasoning model with tool calling capability 
LLM="llama3.1:latest"
```
the result was more interesting than I expected:
```shell
TASK: compute (2 + 4) * 5

--- loop 1 ---
  1. model decided: {'type': 'tool', 'name': 'multiply', 'args': {'a': '(2 + 4)', 'b': '5'}, 'content': ''}
  
  #(...)
  ValueError: invalid literal for int() with base 10: '(2 + 4)'

  # it decided to multiply first and took the entire (2+4) as an argument
```
The model didn't decompose the problem at all. It tried to one-shot the whole thing in a single tool call, handing `'(2 + 4)'` to `multiply` as a literal string.

> [!NOTE]
> **Remember the caution from section 3.3 ?** 
> 
> Back in 3.3, the agent gave a good result even though our protocol fed the model the whole toolset at once. The reasoning model decomposed the expression and sequenced the calls on its own. Swap in a non-reasoning model, like we just did, and the scaffolding we forgot to build becomes visible. 
> 
> Same loop, weaker policy, and the missing scaffolding is suddenly load-bearing.


Now 3 possibilities open:
- We can make the agent self-recover. i.e. wrap the tool call in a try/except, and on failure, feed the error message back to the model as the tool observation.
- We can add some guidance. Right now, the model doesn't know the tools take plain numbers only and that it must work one operation at a time. We can provide guidance by adding a system prompt.
- We can give more information about the tools. When you pass Python functions directly to Ollama as tools, the Python SDK introspects the function signature, type hints, and docstring to generate a JSON Schema tool description. That schema tells the model what tools exist, what each tool does, and what arguments each tool expects (cf. https://ollama.com/blog/functions-as-tools) Just a **reminder**: the SDK/schema tells the model what it may call. It does not run it or execute it. Our runtime is the one doing all that.

{{% details "Ollama JSON schema" %}}
When you pass a Python function to Ollama as a tool, the SDK doesn't send the function. It sends a description of the function, built by introspecting the signature, type hints, and docstring. Here is what the model receives:

```python
from ollama._utils import convert_function_to_tool
import json

def add(a: int, b: int) -> int:
    """Add two numbers
    Args:
      a: The first number
      b: The second number
    Returns:
      The sum of the two numbers
    """
    return int(a) + int(b)

print(json.dumps(convert_function_to_tool(add).model_dump(), indent=2))
```

```json
{
 "type": "function",
 "function": {
   "name": "add",
   "description": "Add two numbers",
   "parameters": {
     "type": "object",
     "defs": null,
     "items": null,
     "required": [
       "a",
       "b"
     ],
     "properties": {
       "a": {
         "type": "integer",
         "items": null,
         "description": "The first number",
         "enum": null
       },
       "b": {
         "type": "integer",
         "items": null,
         "description": "The second number",
         "enum": null
       }
     }
   }
 }
}
```

The model never sees `return int(a) + int(b)`, instead it sees a name, a one-line description, and a typed parameter list. This is how the model "knows" the tools exist and "knows" how to call them.

And it's the same reminder as before: the schema tells the model what it may call; it does not run anything. Our runtime still does all the executing.

Let's print the schema for the function add we used in section 3.3 `def add(a, b): return int(a) + int(b)`

```json
{
  "type": "function",
  "function": {
    "name": "add",
    "description": "",
    "parameters": {
      "type": "object",
      "defs": null,
      "items": null,
      "required": [
        "a",
        "b"
      ],
      "properties": {
        "a": {
          "type": "string",
          "items": null,
          "description": "",
          "enum": null
        },
        "b": {
          "type": "string",
          "items": null,
          "description": "",
          "enum": null
        }
      }
    }
  }
}
```
The param falls back to `string`, and an empty description because there was no docstring to read. 

{{% /details %}}

Given that we've experimented with many settings, let's clean up all the mess following what we've noted and learned from each experiment and from all the documentation and guidelines we've seen.

## 5. Let's build our first LLM Agent
{{% details "Our first LLM Agent" %}}
```python
# Adjust self-recovery, tools, and prompts one by one to see how evey change affects the result.

def add(a: int, b: int) -> int :       
    """Add two numbers
    Args:
      a: The first number
      b: The second number

    Returns:
      The sum of the two numbers
    """
    return int(a) + int(b)

def multiply(a: int, b: int):  
    """Multiply two numbers
    Args:
      a: The first number
      b: The second number

    Returns:
      The product of the two numbers
    """
    return int(a) * int(b)


TOOLS = {"add": add, "multiply": multiply}

import ollama

LLM="llama3.1:latest" # any model is fine, i just had this one already pulled (just make sure the model has tool calling capability)

def real_model(history):
        response = ollama.chat( 
            model=LLM,
            messages=history,
            tools=list(TOOLS.values()),
            options={"temperature": 0}, 
        )
        msg =  response["message"]
        if msg.tool_calls:
            call = msg.tool_calls[0]
            return {"type": "tool", "name": call.function.name, "args": call.function.arguments,
                    "content": msg.content or "", "tool_calls": msg.tool_calls}

        return {"type": "final", "content": response["message"]["content"]}

SYSTEM_PROMPT = """
you have add and multiply, each takes two numbers. 
use a tool for every arithmetic step; your final answer must come only from tool results; never calculate yourself.
"""
#  this is the agent.
def run(task, model, tools, max_steps=10):
    history = [ 
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task}
        ]
    print(f"TASK: {task}\n")

    for step in range(1, max_steps + 1):
        print(f"--- loop {step} ---")
        # 1. ask the model what to do, given everything so far
        action = model(history)
        print(f"  1. model decided: {action}")
        
        # 2. is it a final answer? then we're done
        if action["type"] == "final":
            print("  2. type is 'final' -> returning\n")
            return action["content"], history

        history.append({"role": "assistant", 
                        "content": action.get("content", ""),
                        # this is the caution I talked about in section (3.3.)
                        # our protocol was feeding the whole set of tools to the model
                        "tool_calls": [action["tool_calls"][0]],}) 

        # 3. it is a tool request ? then the runtime executes the tool
        name = action["name"]
        args = action["args"]
        if name not in tools:
            result = f"unknown tool: {name}"
        else:
            try :
                result = tools[name](**args)    
            except Exception as e:
                result = f"tool error in {name}: {type(e).__name__}: {e}"

        print(f"  3. ran tool {name}({args}) -> {result}")
        # 4. append the result to history, then loop back to step 1
        history.append({"role": "tool", 
                        "name": name,
                        "args":args, 
                        "content": str(result)})
        print(f"  4. appended result; history now has {len(history)} messages\n")
        print("history now is : " , history)
        print("\n\n")

    raise RuntimeError("agent did not finish — it looped")

if __name__ == "__main__":
    answer, _ = run("compute (2 + 4) * 5", real_model, TOOLS)
    print(answer)

```
{{% /details %}}

Let's look at its trace (I added print history to the log ):
```shell
TASK: compute (2 + 4) * 5

--- loop 1 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': 2, 'b': 4}, 'content': '', 
  'tool_calls': [
    ToolCall(function=Function(name='add', arguments={'a': 2, 'b': 4})), 
    ToolCall(function=Function(name='multiply', arguments={'a': 'result of add(2, 4)', 'b': 5}))]}
  3. ran tool add({'a': 2, 'b': 4}) -> 6
  4. appended result; history now has 4 messages

history now is :  [
    {'role': 'system', 'content': '\nyou have add and multiply, each takes two numbers. \nuse a tool for every arithmetic step; your final answer must come only from tool results; never calculate yourself.\n'}, 
    {'role': 'user', 'content': 'compute (2 + 4) * 5'}, 
    {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': 2, 'b': 4}))]}, 
    {'role': 'tool', 'name': 'add', 'args': {'a': 2, 'b': 4}, 'content': '6'}]



--- loop 2 ---
  1. model decided: {'type': 'tool', 'name': 'multiply', 'args': {'b': 5, 'a': 6}, 'content': '', 'tool_calls': [ToolCall(function=Function(name='multiply', arguments={'b': 5, 'a': 6}))]}
  3. ran tool multiply({'b': 5, 'a': 6}) -> 30
  4. appended result; history now has 6 messages

history now is :  [
    {'role': 'system', 'content': '\nyou have add and multiply, each takes two numbers. \nuse a tool for every arithmetic step; your final answer must come only from tool results; never calculate yourself.\n'}, 
    {'role': 'user', 'content': 'compute (2 + 4) * 5'}, 
    {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': 2, 'b': 4}))]}, 
    {'role': 'tool', 'name': 'add', 'args': {'a': 2, 'b': 4}, 'content': '6'}, 
    {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='multiply', arguments={'b': 5, 'a': 6}))]}, 
    {'role': 'tool', 'name': 'multiply', 'args': {'b': 5, 'a': 6}, 'content': '30'}]



--- loop 3 ---
  1. model decided: {'type': 'final', 'content': 'The result of (2 + 4) * 5 is 30.'}
  2. type is 'final' -> returning

The result of (2 + 4) * 5 is 30.
```

> [!CAUTION]
> **Interesting.** The assistant now follows the instructions and uses the provided tools. 

> [!DEFAULT]
> **The history was rebuilt:** 
>
> The chain is grounded because history is well built and the trace shows it cleanly. 
> Notice how in `Loop 1` the model still proposed `[add, multiply('result of add(2,4)', 5)]` like we saw in section 4.3. But because we now store only `tool_calls[0]` in the assistant turn, we steered it into a proper single tool call in `Loop 2`. The loop protocol corrected for the model's bad habit.
>
> **The arg types were never random:** 
>
> This is the first time we have a trace showing `'args': {'a': 2, 'b': 4}`. In section 3.3 we used untyped tools `def add(a, b)` so the model fills the args as strings `{'a': '2', 'b': '4'}`. Here the tools are typed `def add(a: int, b: int)`, the schema declares `"type": "integer"` (*see the "Ollama JSON schema" fold in section 4.3*), and the model answers with ints. 
>
> **The stop problem, revisited:**
>
> Another element worth noticing is the "stop problem" we encountered in section 4.1, where the model had the answer at loop 2 and still didn't stop until loop 10. We blamed two things: a mangled history, and the fact that producing an answer and deciding to stop are two different acts. Here the agent stopped at loop 3. We fixed both causes, and it's worth being precise about which did what:
> - History is now faithful: We store the real tool_calls in the assistant turn, so the model sees its own past actions instead of being handed amnesia every loop. With a true transcript it can tell the work is already done.
> - The system prompt gives final a definition: "your final answer must come only from tool results" turns the fuzzy "am I done?" into a checkable condition: once a tool has produced the number, there is nothing left to do but report it.
>
> What we did not do is add a hard stop tool. Stopping is still the model's call, we just stopped sabotaging it. `max_steps` stays underneath as the seatbelt: a real stop condition, not a stop strategy.
>

Let's do one last test to really be sure our agent is truly grounded. Let's change multiply with a fixed output and see if model binds by it:
```python
def multiply(a: int, b: int):  
    """Multiply two numbers
    Args:
      a: The first number
      b: The second number

    Returns:
      The product of the two numbers
    """
    return 95
```

```shell
TASK: compute (2 + 4) * 5

--- loop 1 ---
  1. model decided: {'type': 'tool', 'name': 'add', 'args': {'a': 2, 'b': 4}, 'content': '', 
  'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': 2, 'b': 4})), 
  ToolCall(function=Function(name='multiply', arguments={'a': 'result of add(2, 4)', 'b': 5}))]}
  3. ran tool add({'a': 2, 'b': 4}) -> 6
  4. appended result; history now has 4 messages

history now is :  [
    {'role': 'system', 'content': '\nyou have add and multiply, each takes two numbers. \nuse a tool for every arithmetic step; your final answer must come only from tool results; never calculate yourself.\n'}, 
    {'role': 'user', 'content': 'compute (2 + 4) * 5'}, 
    {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': 2, 'b': 4}))]}, 
    {'role': 'tool', 'name': 'add', 'args': {'a': 2, 'b': 4}, 'content': '6'}]



--- loop 2 ---
  1. model decided: {'type': 'tool', 'name': 'multiply', 'args': {'a': 6, 'b': 5}, 'content': '', 'tool_calls': [ToolCall(function=Function(name='multiply', arguments={'a': 6, 'b': 5}))]}
  3. ran tool multiply({'a': 6, 'b': 5}) -> 95
  4. appended result; history now has 6 messages

history now is :  [
    {'role': 'system', 'content': '\nyou have add and multiply, each takes two numbers. \nuse a tool for every arithmetic step; your final answer must come only from tool results; never calculate yourself.\n'}, 
    {'role': 'user', 'content': 'compute (2 + 4) * 5'}, 
    {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='add', arguments={'a': 2, 'b': 4}))]}, 
    {'role': 'tool', 'name': 'add', 'args': {'a': 2, 'b': 4}, 'content': '6'}, 
    {'role': 'assistant', 'content': '', 'tool_calls': [ToolCall(function=Function(name='multiply', arguments={'a': 6, 'b': 5}))]}, 
    {'role': 'tool', 'name': 'multiply', 'args': {'a': 6, 'b': 5}, 'content': '95'}]



--- loop 3 ---
  1. model decided: {'type': 'final', 'content': 'The result of (2 + 4) * 5 is 95.'}
  2. type is 'final' -> returning

The result of (2 + 4) * 5 is 95.

```
> [!CAUTION]
> **Experiment.** Will a reasoning model also give the answer 95 ? try it and see !



## 1st Milestone : We have a real agent

In section 3, we threw everything that does not contain the essential algorithmic content of an agent and promised to add it back step-by-step only if the bare loop demanded it. We did it and we now have a real agent: it chains, acts on what it observed, and stops. It's the same `act, observe, act again` kernel the fake model had, now driven by weights instead of an `if`. **So where does this loop stop being enough ?**

1. when the transcript outgrows the window : in our previous traces, we can see `len(history)` climb little by little. Once we scale to hundreds of messages, we will easily slide past the context limit and the model might forget what it's doing in the first place. The fix is to stop pasting the full history back every loop: summarize old turns, or retrieve only the relevant few. That is what "memory" and RAG are. You add it when the loop drops something, not before.


2. when one straight list can't hold the work : the `history` we built is a single thread: one model, one conversation, one step at a time. If we want to add parallel subtasks that don't depend on each other or a tool that returns a megabyte, this single transcript will stop being the right structure. The fix is a sub-agent: another run() with its own history, handed one job, returning a short summary. A "multi-agent system" is this same loop, nested.

Each item we discarded in section 3 returns as the answer to one specific failure of the bare loop. In my opinion, this order matters: reach for the loop first, let it break in a trace, then add the one part that break requires.

{{% details "Appendix: Anatomy of an agent" %}}
**`model:`** 
- maps `history -> next action` (a tool call, or `final`). This is the only part that "decides". Everything else just carries out the decision. 
- **Pro:** fully replaceable. 
- **Con:** it's also where the mess came from. And it only knows what we put in `history` so feed it a bad transcript and it will make bad calls. 


**`tools:`**
 - python functions the model is allowed to *name* but not see inside. the agent's entire reach into the world is this dictionary. 
- **Pro:** extending the agent = adding one function to the dict. 
- **Con:** with no proper guidance and documentation, the model can start guessing how to call them. 


**`executor:`**
- it's the `tools[name](**args)` part where a named action becomes a real call. this is the bridge between thinking and doing. 
- **Pro:** all the danger is localized to a single line, which is exactly why safety is something we can actually reason about here.
- **Con:** all the danger is localized to a single line ! right now it runs whatever the model names, with whatever args. needs to be air-tight, with proper validation, testing and security. 


**`loop:`** 
- is the `run()` cycle: ask, act, append, repeat, until `final` or `max_steps`. 
- **Pro:** tiny, transparent, model-agnostic. 
- **Con:** termination is a blunt instrument (`max_steps` is a seatbelt), and our append step mangled the assistant turn. Unbounded growth will also eventually blow the context window. 

{{% /details %}}




