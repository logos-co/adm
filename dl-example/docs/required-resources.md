# Resources for Robust Human–Machine Project Portfolio Selection
To implement the Robust Human–Machine Framework for Project Portfolio Selection (PPSS), as described in the sources [1, 2], you will need to gather several types of resources for each project, as well as the necessary infrastructure and human expertise.
Here's a breakdown of the appropriate resources to gather:
1. Human Expertise and Stakeholder Involvement [3]:
    ◦ Experienced Experts, Decision-Makers (DMs), and Stakeholders: These individuals are crucial for participating in the qualitative evaluation of projects. Their input, provided as linear qualitative evaluations rather than exact numerical values, forms the basis for defining project value [3].
2. Project-Specific Data and Information [4-7]: For each candidate project (p_i), the following attributes and constraint information are essential:
    - Construction Duration (d_i): The estimated time required to complete project p_i [4].
    - Construction Cost (c_i): The financial expenditure associated with project p_i [4].
    - Multiple Project Values (v_ij): Values corresponding to the decision-maker's various requirements (e.g., v_i1, v_i2, ..., v_iJ for J types of values) [4].
    - Uniqueness Constraint: Information ensuring that each project is executed at most once [5].
    - Cost Constraint: Data on how each project's cost contributes to the total cost for each year (t) to ensure it does not exceed the budget (B_t) [5].
    - Cooperation Constraint (H(p_i)): Identification of subsets of projects where benefits are interdependent, without a strict sequence of construction times [5, 6].
    - Precedence Constraint (Ψ(p_i)): Identification of projects that must be completed before project p_i can commence [6].
    - Exclusive Constraint (Φ(p_i)): Identification of projects that are mutually exclusive with p_i and cannot be undertaken simultaneously [7].
    - Qualitative Evaluations: Unstructured qualitative evaluations from human experts and stakeholders regarding various aspects of a project's value or comparisons between multiple projects [3, 8]. These evaluations will be mathematically modeled as linear equations or inequalities [8].
3. Computational Infrastructure and Software Environment [9]:
    - Hardware: A powerful computing system is required, as demonstrated by the experimental setup which used a PC with a 2.5-GHz Intel Core i9 processor, 16 GB of RAM, and 16 GB of memory [9].
    - Software Libraries and Programming Language: 
        * Python 3.9: The programming language used for implementation [9]. 
        * PyTorch 2.3.1: A deep learning framework used as the backend for implementing the Deep Neural Network (DNN) [9]. 
        * Adam Optimizer: Utilized for training neural networks to facilitate faster algorithm convergence [9, 10].
4. Algorithmic and Data Management Components [3, 11-13]:
    - Qualitative Evaluation Translation Module: Software or algorithms capable of converting human qualitative evaluations into linear equality or inequality constraints that define a convex polytope representing the feasible space for the project value matrix [3, 14].
    - Robust Evaluation Criteria Module: Implementation of algorithms to compare the dominance relationships between two solutions (project portfolios) by evaluating a finite number of boundary points (ext(V_j)) of the convex polytope, as enumerating all values in a continuous vector space is not feasible [15-17].
    - Deep Preference-based Q Network (DPbQN) Model: This is the core optimization algorithm [2, 3], which requires:  
        * Deep Neural Network (DNN): A multi-layered network designed to fit Q-values for state-action pairs. It includes an input layer to transform the two-dimensional state matrix into a one-dimensional vector, dense hidden layers using the ReLu activation function for efficiency, and an output layer with a Linear activation function [18-20]. 
        * Experience Pool (D): A database to store training information in the form of "data labels" (σ1, σ2, µ). These labels represent paired comparisons of sequences of states and actions, indicating dominance (σ1 ≻ σ2, µ=1), inferiority (σ1 ≺ σ2, µ=0), or equivalence (σ1 ∼ σ2, µ=0.5) based on the robust evaluation criteria [12, 13, 21]. 
        * Reinforcement Learning Components: Implementation of the ϵ-greedy strategy for action selection, the defined loss function (Equation 15, based on the Bradley–Terry model and Luce–Shephard choice rule), and the gradient descent method for training and updating network parameters [13, 21, 22].