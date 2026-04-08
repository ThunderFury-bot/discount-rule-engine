Reflection & Write-Up
o Why you chose your approach.
o What challenges you see if the number of rules grows to 20+.
o How you would improve or refactor your design to handle more rules.


While designing this project, I chose a rule-based architecture using object-oriented principles. Each discount rule is implemented as a separate class that follows a common interface. This approach made the system clean and easy to understand because every rule is independent and has its own logic. I also used a priority-based system so that only the most important applicable rule gets applied, which simplifies decision-making and avoids conflicts between multiple rules.

One of the main challenges I can see in the future is when the number of rules increases to 20 or more. In that case, managing priorities manually can become difficult and error-prone. Also, iterating through all rules for every request might impact performance. Another issue could be maintainability, as adding or modifying rules frequently may lead to confusion if not properly organized.

To improve the design for larger systems, I would consider storing rules in a database or configuration file instead of hardcoding them. I could also introduce a rule grouping or tagging system to manage them better. For performance, caching frequently used rules or optimizing the evaluation process would help. Additionally, I would explore using a more advanced pattern like a decision tree or rule engine framework to make the system more scalable and efficient.

Overall, this approach works well for small to medium-scale applications, and with some enhancements, it can be extended to handle more complex scenarios.