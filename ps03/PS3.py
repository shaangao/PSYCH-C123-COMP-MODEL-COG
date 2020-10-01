#!/usr/bin/env python
# coding: utf-8

# <div style="background-color: #c1f2a5">
# 
# 
# # PS3 
# 
# The idea of reasoning by following simple rules provides an attractively straightforward characterization of cognition. However, production systems can be very difficult to design in ways that are guaranteed to always work. In this problem, you will write some functions to help you work with production systems, and then you will use those functions to reason about several different sets of rules.
# 
# # Instructions
# 
# 
# 
# Remember to do your problem set in Python 3. Fill in `#YOUR CODE HERE`.
# 
# Make sure: 
# - that all plots are scaled in such a way that you can see what is going on, and 
# - that the general patterns are fairly represented.
# - to label all x- and y-axes, and to include a title.
# 
# 
# </div>

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# We will represent a set of beliefs using Python sets: Each element in the set corresponds to a true proposition. 
# 
# As a quick refresher, Python sets are **unique, unordered collections** of objects. You can check if an item is in a set with the `in` keyword, and you can add new things to the set using the `.add()` method, for example:
# 
# For example, the following belief states that `'a'` and `'b'` are true propositions. We then add `'c'` as another true proposition.
# 

# In[2]:


example_belief = {'a', 'b'}
print('a' in example_belief)
print('c' in example_belief)


# In[3]:


example_belief.add('c')
example_belief


# So, our beliefs will be represented using sets and the rules of our production system using a list of 2-tuples, where each tuple contains a *condition* and a *result*. The rule can only 
# be applied if the condition is present in the set of beliefs; if the rule is applied, then the result should be added to the set of beliefs. For example, the following belief again consists of `'a'` and `'b'`, and the rules state that `"if a, then b"` and that `"if c, then d"`. To help visualize the rules a bit better, we include a function called `print_rules` that will print out each rule on a separate line:

# In[4]:


example_belief = {'a', 'b'}
example_rules = [('a', 'b'), ('c', 'd')]

def print_rules(rules):
    for rule in rules:
        print(str(rule[0]) + " --> " + str(rule[1]))
        
print_rules(example_rules)


# ## Q1.1 [5pts, HELP] 
# Using the representation of beliefs and rules specified above, write a function called <code>match</code> that searches through a given list of rules to find a rule that is triggered by the given set of beliefs.

# In[5]:


def match(belief, rules):
    """Determine whether a rule is triggered by the given set of beliefs.

    The *first* rule in the list of rules that is triggered should be
    returned (and you should only ever return one rule, even if multiple are
    triggered). If no rule is triggered, `None` should be returned.

    A rule should only be triggered if it adds something new to the set of 
    beliefs: For example, if the beliefs are `{'a', 'b'}`, and there is only 
    one rule, `('a', 'b')`, then it should *not* be triggered because it 
    doesn't add anything new. If the beliefs were just `{'a'}`, however, then 
    the rule *should* be triggered because it would add a new belief `b` to 
    the set of beliefs.

    
    Parameters
    ----------
    belief : set
        A set of true propositions.
    rules : list of tuples
        A list of tuples, such that for each tuple, the first element implies
        the second (but not vice versa).
        
    Returns
    -------
    The first rule (tuple) that was triggered, or `None` if no rules were triggered.
    
    """
    
    # YOUR CODE HERE
    for rule in rules:
        if rule[0] in belief and rule[1] not in belief:
            return rule
    return None


# 
# ## Q1.2. [5pts, SOLO] 
# Test your function on a few test cases, and report the results in Gradescope.

# In[6]:


print('Q1.2.a')
print(match({'a'}, [('a', 'b')]), ('a', 'b'))

print('Q1.2.b')
print(match({'b'}, [('a', 'b')]))

print('Q1.2.c')
print(match({'a', 'b'}, [('a', 'b')]))

print('Q1.2.d')
print(match({'a'}, [('a', 'b'), ('b', 'c')]))

print('Q1.2.e')
print(match({'a', 'b'}, [('a', 'b'), ('b', 'c')]))

print('Q1.2.f')
print(match({'a', 'b', 'c'}, [('a', 'b'), ('b', 'c')]))


# ## Q2.1 [5pts, SOLO] 
# Now that we have a way to trigger rules based on a set of beliefs, we want to engage in a process called [forward chaining](http://en.wikipedia.org/wiki/Forward_chaining). The idea behind forward chaining is that we want to execute rules that are triggered by our beliefs, and to continue triggering rules until no more can be triggered. For example, if we have:
# 
# ```python
# rules = [("belief1", "belief2"), ("belief2", "belief3")]
# belief = {"belief1"}
# ```
# 
# To start out, we have `belief_1`, but we also have a rule "if `belief_1`, then `belief_2`", so we should update our belief with `belief_2`.
# 
# Then, we have *another* rule that says "if `belief_2`, then `belief_3`". Because our belief now consists of both `belief_1` and `belief_2` (due to triggering the first rule), this second rule should also be triggered, and should add `belief_3` to our total set of beliefs.

# Write a function, <code>forward_chain</code>, to automatically perform forward chaining with a given set of initial beliefs and rules using your previous <code>match</code> function. Make sure your function does in fact perform full forward chaining &mdash; i.e., if there are two matching rules but only one matches at the beginning, they should still both be triggered!

# In[10]:


def forward_chain(belief, rules):
    """Fully execute a set of given rules that match a given belief, until
    no more new rules are triggered. That is, this function should:
    (i) Scan through the rules until it finds rule(s) which are applicable,
    (ii) trigger such rules and update beliefs,
    (iii) repeat (i) and (ii) until no further rules can be triggered.
    
    Returns a new set of beliefs (without changing the original set of beliefs) 
    based on which rules were triggered.

    Note: This function should employ a `while` loop and should call the `match` 
    function you implemented in the first part of this problem.

    Hint: You should be able to do this in 8 lines of code, including the
    return statement.
    
    Parameters
    ----------
    belief : set
        A set of true propositions.
    rules : list of tuples
        A list of tuples, such that for each tuple, the first element implies
        the second (but not vice versa).
        
    Returns
    -------
    tuple of (new_belief, triggered_rules):
        new_belief is an updated set of true propositions, and triggered_rules
        is the list of rules that were triggered, in order.
        
    """
    # YOUR CODE HERE
    new_belief = belief.copy()
    triggered_rules = []
    while rules:
        triggered = match(new_belief, rules)
        if triggered == None:
            break
        triggered_rules += [triggered]
        new_belief.add(triggered[1])
        rules.remove(triggered)
    return (new_belief, triggered_rules)


# In[11]:


# test your function
b, r = forward_chain({'a'}, [('a', 'b'), ('b', 'c')])
print_rules(r) # should print both 'a --> b' and 'b --> c'
b             # should be {'a', 'b', 'c'}
# add your own test cases here!


# ## Q2.2. [5pts, SOLO] 
# Test your function on a few test cases, and report the results in Gradescope.

# In[13]:


b, r = forward_chain({'a'}, [('a', 'b'), ('b', 'c'), ('c', 'd')])
print('Q2.2.a')
print(b)
print_rules(r)


b, r = forward_chain({'a'}, [('b', 'c'), ('c', 'd'), ('a', 'b')])
print('Q2.2.b')
print(b)
print_rules(r)

b, r = forward_chain({'a'}, [('a', 'c'), ('a', 'b')])
print('Q2.2.c')
print(b)
print_rules(r)

b, r = forward_chain({'b'}, [('a', 'b'), ('b', 'c')])
print('Q2.2.d')
print(b)
print_rules(r)

b, r = forward_chain({'a', 'b', 'c'}, [('b', 'c'), ('b', 'a'), ('a', 'b')])
print('Q2.2.e')
print(b)
print_rules(r)

b, r = forward_chain(set(), [('b', 'c'), ('b', 'a'), ('a', 'b')])
print('Q2.2.f')
print(b)
print_rules(r)


# ## Q3.1 [5pts, HELP] 
# Imagine you have a small sprinkler that can water your grass but does not reach the path you walk on or your car. However, if it rains, then the car and the path both get wet. The sprinkler definitely comes on if the appropriate switch is flipped. We might try to capture this information in a production system as follows:
# 
#     IF switch is flipped THEN sprinkler was on
#     IF sprinkler was on THEN grass is wet
#     IF it rained THEN car is wet
#     IF it rained THEN path is slippery
#     IF it rained THEN grass is wet
# 
# If you now observed `switch is flipped` but nothing else, what would the above production system lead you to conclude? 
# Tips:
# - Define the rule system described above as `rules_1`
# - Define your initial belief as `{'switch is flipped'}`
# - Use your `forward_chain` function to find out the final belief `belief_final` and the triggered rules `triggered_rules`
# 
# Report in Gradescope the final belief and the triggered rules.

# In[18]:


#YOUR CODE HERE
rules_1 = [('switch is flipped', 'sprinkler was on'), ('sprinkler was on', 'grass is wet'), 
           ('it rained', 'car is wet'), ('it rained', 'path is slippery'), ('it rained', 'grass is wet')]
belief_initial = {'switch is flipped'}
belief_final, triggered_rules = forward_chain(belief_initial, rules_1)

# show final belief
print(belief_final)
#show triggered rules
print_rules(triggered_rules)


# ## Q3.2. [5pts, SOLO] 
# 
# 
# In words, what do the production rules have to say about the states of the sprinkler, grass, your car, and the path you walk on, given you observed that the switch is flipped? Be careful to **only** report beliefs that are justified by your observations and the triggered rules of our production system and _not_ what you personally believe! Write your answer in Gradescope.

# A: 
# 
# Since I observed that the switch is flipped, I will have an initial belief "switch is flipped" which is justified by this observation. I can then infer from this initial belief by triggering the rule "IF switch is flipped THEN sprinkler was on" that the sprinkler was on. Since now I have the belief that "sprinkler was on," I can further trigger the rule "IF sprinkler was on THEN grass is wet" to infer that grass is wet. No other production rules in this system will be triggered, therefore resulting in a set of new beliefs including "switch is flipped," "sprinkler was on," and "grass is wet." No inferences regarding my car and path can be made.

# ## Q4.1 [2pts, SOLO] 
# For this next section, let's imagine a different production system that is similar but ultimately **unrelated** to the one we defined in Q3.1:
# 
#     IF sprinkler was on THEN switch is flipped
#     IF car is wet THEN it rained
#     IF path is slippery THEN it rained
#     IF grass is wet THEN it rained
# 
# In this new production system, if you knew only that the grass is wet, what would you conclude? Again, you can use your `forward_chain` function to find out.
# 
# Report in Gradescope the final belief and the triggered rules.

# In[19]:


#YOUR CODE HERE
rules_2 = [("sprinkler was on", "switch is flipped"), ("car is wet", "it rained"), 
           ("path is slippery", "it rained"), ("grass is wet", "it rained")]
belief_initial = {'grass is wet'}
belief_final, triggered_rules = forward_chain(belief_initial, rules_2)

# show final belief
print(belief_final)
#show triggered rules
print_rules(triggered_rules)


# ## Q4.2. [5pts, SOLO] 
# What conclusion(s) do you draw based on this new scenario shown in Q4.1? Intuitively, do they seem like valid or reasonable inferences to make given the rules of your production system? Please write down your explanation in Gradescope.

# A: 
# 
# Since I observed that the grass is wet, I will have an initial belief "grass is wet" which is justified by this observation. I can then trigger the rule "IF grass is wet THEN it rained" to infer that it rained. No other production rules in this system will be triggered, therefore resulting in a set of new beliefs including "grass is wet," "it rained."
# 
# Intuitively, they seem like reasonable inferences to make given the rules of the production system. Because grass is normally dry; if it is wet somehow, there should be a cause, and "it rained" seems a highly likely one if there is no additional information given (such as "there is a sprinkler for watering the grass and it is turned on" and "the car and path are dry") that can also cause the grass to be wet and/or rule out the effect of rain. (Since Q4 is supposed to be unrelated to Q3, in Q4 we do not know if there is a sprinkler which can always wet the grass; so the spinkler explanation should be far less likely than the rain explanation.)

# ## Q5.1 [2pts, SOLO] 
# Finally, we can imagine a third production system where the rules apply in both directions:
# 
#     IF switch is flipped THEN sprinkler was on
#     IF sprinkler was on THEN grass is wet
#     IF it is raining THEN car is wet
#     IF it is raining THEN path is slippery
#     IF it is raining THEN grass is wet
#     IF sprinkler was on THEN switch is flipped
#     IF car is wet THEN it is raining
#     IF path is slippery THEN it is raining
#     IF grass is wet THEN it is raining
# 
# If you observed `sprinkler was on`, what would you conclude? You can again use `forward_chain`. 
# 
# Report in Gradescope the final belief and the triggered rules.

# In[20]:


#YOUR CODE HERE
rules_3 = [('switch is flipped', 'sprinkler was on'), ('sprinkler was on', 'grass is wet'), 
           ('it is raining', 'car is wet'), ('it is raining', 'path is slippery'), ('it is raining', 'grass is wet'),
           ("sprinkler was on", "switch is flipped"), ("car is wet", "it is raining"), 
           ("path is slippery", "it is raining"), ("grass is wet", "it is raining")]
belief_initial = {'sprinkler was on'}
belief_final, triggered_rules = forward_chain(belief_initial, rules_3)

# show final belief
print(belief_final)
#show triggered rules
print_rules(triggered_rules)


# ## Q5.2 [5pts, SOLO]
# 
# 1) Do these conclusions from Q5.1 match your intuitions about what inferences should or should not be valid? Explain your reasoning.
# 
# 2) What does this tell us about the limitations of production systems? 
# 
# Please write down your answers to both questions in Gradescope.

# A:
# 
# 1) No, these conclusions do not match my intuitions about what inferences should or should not be valid. Intuitively, I will only appply two rules: "IF sprinkler was on THEN grass is wet" and "IF sprinkler was on THEN switch is flipped;" therefore my intuitive final beliefs would be: "sprinkler was on," "grass is wet," and "switch is flipped." I will not make the inference "it is raining," nor make further inferences based on "it is raining," i.e., "car is wet" and "path is slippery." Because if I already know the rule "IF sprinkler was on THEN grass is wet" and I have the beliefs that "sprinkler was on" and "grass is wet," I will mostly likely attributute "grass is wet" to what I already observed -- "sprinkler was on," and do not attribute it to "raining" anymore (because "sprinkler was on" can already explain the wet grass very well), especially when there is no additional information (e.g., I also observed wet car and wet path, and the sprinker cannot reach the car and the path) suggesting that the wet grass may not be caused by the operating sprinkler.
# 
# 2) Limitations of production systems: The process that a production system generates new beliefs is pretty much linear -- applying rules one by one whenever the condition of a rule is satisfied; it does not take into account other information in the set of beliefs that are not directly related to the condition of the current rule being applied, and therefore will miss important contextual information that may alter the plausibility of certain inferences. For example, in Q5, when the rule "IF grass is wet THEN it is raining" is applied, the production system does not take into account the contextual information that "sprinkler was on" and that wet grass can already be explained successfully with an operating sprinkler (because "IF sprinkler was on THEN grass is wet"), which makes other causal inferences for the wet grass unlikely in the absence of additional information. 

# <div style="background-color: #c1f2a5">
# 
# # Submission
# 
# When you're done with your problem set, do the following:
# - Upload your answers in Gradescope's PS3.
# 
# - Convert your Jupyter Notebook into a `.py` file by doing so:    
#     
# </div>
# 
# 
# <center>    
#   <img src="https://www.dropbox.com/s/7s189m4dsvu5j65/instruction.png?dl=1" width="300"/>
# </center>
# 
# <div style="background-color: #c1f2a5">
#     
# - Submit the `.py` file you just created in Gradescope's PS2-code.
#     
# </div>        
# 
# 
# 
# 
# </div>
# 
# </div>
# 

# In[ ]:




