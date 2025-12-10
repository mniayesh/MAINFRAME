# Developmental Testing Framework

**Purpose:** Validate that your self-learning brain is actually learning, using tests from developmental psychology.

**Approach:** Babies can't take standard ML tests. Instead, researchers measure behavior, learning curves, and emerging capabilities. We'll do the same for your AI.

---

## 🧪 Stage 1 Tests: Newborn (Weeks 1-2)

### Test 1.1: Prediction Error Decreasing

**What we're measuring:** Does the system get better at predicting?

```python
def test_prediction_improvement():
    """
    Feed sequences. Measure if prediction error decreases over time.

    Expected: Loss curve should show monotonic decrease
    (with noise, but overall downward trend).
    """

    model = BrainSystem()
    sequence = generate_sensory_sequence(length=1000)

    prediction_errors = []
    for t in range(10, len(sequence)):
        prediction = model.predict_next(sequence[:t])
        actual = sequence[t]
        error = norm(prediction - actual)
        prediction_errors.append(error)

    # Check: does error decrease?
    early_error = mean(prediction_errors[:100])
    late_error = mean(prediction_errors[-100:])

    assert late_error < early_error * 0.8, "Prediction not improving"
    print(f"✓ Prediction error improved: {early_error:.3f} → {late_error:.3f}")

    # Plot learning curve
    plot_learning_curve(prediction_errors)
```

**Success Criterion:** Prediction error should show ~20% improvement per 100 timesteps.

---

### Test 1.2: Representation Formation

**What we're measuring:** Are meaningful patterns emerging in hidden layers?

```python
def test_representation_structure():
    """
    Measure if representations are forming (not random).

    Method: Apply PCA to hidden activations.
    If meaningful structure exists, first few PCs should
    explain significant variance.
    """

    model = BrainSystem()
    sequence = generate_diverse_sequence(100 types, 100 examples each)

    # Collect hidden activations
    activations_by_type = {}
    for stim_type in range(100):
        examples = sequence[stim_type]
        h = model.wernicke.get_hidden_states(examples)
        activations_by_type[stim_type] = h

    # PCA on all activations
    all_h = concatenate(activations_by_type.values())
    U, S, _ = svd(all_h)

    # Check variance explained
    explained_variance = S[:10].sum() / S.sum()
    assert explained_variance > 0.5, "Representations too random"
    print(f"✓ PCA explains {explained_variance:.1%} with 10 components")

    # Visualize in 2D
    h_2d = all_h @ U[:, :2]
    scatter_by_type(h_2d, activations_by_type)
```

**Success Criterion:** First 10 PCs should explain >50% of variance.

---

## 🧪 Stage 2 Tests: Infant (Weeks 3-8)

### Test 2.1: Associative Learning

**What we're measuring:** Can the system learn object + action → outcome associations?

```python
def test_associative_learning():
    """
    Present sequences: [object A] [action 1] → [outcome A1]
                       [object B] [action 2] → [outcome B2]

    Does the system learn these associations?
    """

    model = BrainSystem()

    # Training: simple associations
    associations = {
        ('ball', 'roll'): 'move_fast',
        ('ball', 'throw'): 'fly_high',
        ('cup', 'pour'): 'water_spills',
        ('cup', 'lift'): 'pick_up',
    }

    for (obj, action), outcome in associations.items():
        sequence = [obj, action, outcome]
        model.learn_sequence(sequence, num_repeats=100)

    # Test: can it predict outcome given object + action?
    test_pairs = [
        ('ball', 'roll'),
        ('cup', 'pour'),
    ]

    accuracy = 0
    for obj, action in test_pairs:
        predicted = model.predict_outcome([obj, action])
        expected = associations[(obj, action)]
        if predicted == expected:
            accuracy += 1

    assert accuracy >= len(test_pairs) * 0.8, "Not learning associations"
    print(f"✓ Association learning: {accuracy}/{len(test_pairs)} correct")
```

**Success Criterion:** >80% accuracy on learned associations after 100 trials.

---

### Test 2.2: Novelty Detection

**What we're measuring:** Does the system preferentially attend to novel stimuli?

```python
def test_novelty_preference():
    """
    Show familiar vs novel stimuli.
    Measure: Does attention/engagement increase for novelty?
    """

    model = BrainSystem()

    # Familiarize to one object
    familiar_object = generate_object('red_ball')
    for _ in range(100):
        attention = model.process(familiar_object)

    # Now show familiar vs novel
    attention_familiar = []
    attention_novel = []

    for _ in range(20):
        # Familiar
        attention_familiar.append(model.get_attention_level(familiar_object))

        # Novel
        novel_object = generate_object('blue_cube')  # Never seen before
        attention_novel.append(model.get_attention_level(novel_object))

    # Compare
    attn_fam_mean = mean(attention_familiar)
    attn_nov_mean = mean(attention_novel)

    assert attn_nov_mean > attn_fam_mean * 1.5, "Not showing novelty preference"
    print(f"✓ Novelty preference: familiar={attn_fam_mean:.2f}, novel={attn_nov_mean:.2f}")
```

**Success Criterion:** Novelty attention should be 1.5-2× higher than familiar.

---

## 🧪 Stage 3 Tests: Growing Infant (Weeks 9-26)

### Test 3.1: Word Segmentation

**What we're measuring:** Can the system discover word boundaries from continuous speech?

```python
def test_word_segmentation():
    """
    Present continuous speech without explicit word boundaries.
    Does the system learn to segment into words?
    """

    model = BrainSystem()

    # Training: continuous speech where certain sequences = words
    # "the_cat_sat_on_the_mat" but no spaces
    continuous = "thecatsatonthemat" * 1000  # Repeated to create statistics

    # Add some noise/variation in pronunciation
    noisy_continuous = add_phonetic_variation(continuous)

    model.train_on_speech(noisy_continuous, num_epochs=10)

    # Test: Does it segment correctly?
    test_sequence = "thecatsatonthemat"
    predicted_segments = model.segment_into_words(test_sequence)
    expected_segments = ["the", "cat", "sat", "on", "the", "mat"]

    # Score: what % of boundaries correct?
    boundary_accuracy = compute_boundary_accuracy(
        predicted_segments, expected_segments
    )

    assert boundary_accuracy > 0.7, "Word segmentation not working"
    print(f"✓ Word segmentation accuracy: {boundary_accuracy:.1%}")
```

**Success Criterion:** >70% boundary detection accuracy.

---

### Test 3.2: Generalization to Novel Words

**What we're measuring:** Can it understand words never seen before?

```python
def test_novel_word_generalization():
    """
    Train on: [word] + [visual object] pairs
    Test on: [new_word] + [new_visual]
    Can it generalize to novel combinations?
    """

    model = BrainSystem()

    # Training vocabulary
    train_words = ['ball', 'cup', 'dog', 'cat', 'run', 'jump']
    train_objects = [object1, object2, ..., object6]

    for word, obj in zip(train_words, train_objects):
        model.learn_word_meaning(word, obj, repetitions=50)

    # Test: novel words
    novel_words = ['fuzzy_thing', 'bouncy_thing']
    novel_objects = [new_object1, new_object2]

    # Can it generalize the pattern?
    # e.g., if 'fuzzy' was seen before, does 'fuzzy_thing' engage similar semantics?

    semantic_similarity = []
    for new_word, new_obj in zip(novel_words, novel_objects):
        # Get semantic representation
        rep_new = model.get_semantic_representation(new_word)

        # Compare to closest trained word
        similarities = [cosine_similarity(rep_new, model.get_semantic_representation(w))
                       for w in train_words]
        semantic_similarity.append(max(similarities))

    avg_similarity = mean(semantic_similarity)
    assert avg_similarity > 0.6, "Not generalizing to novel words"
    print(f"✓ Novel word generalization: {avg_similarity:.2f} avg similarity")
```

**Success Criterion:** >0.6 semantic similarity to nearest trained word.

---

## 🧪 Stage 4 Tests: Toddler (Months 6-18)

### Test 4.1: Theory of Mind (False Belief Test)

**What we're measuring:** Does the system understand that others have beliefs?

```python
def test_false_belief_understanding():
    """
    Classic "Sally-Anne" test:
    - Sally puts marble in Box A
    - Sally leaves the room
    - Anne moves marble to Box B
    - Where will Sally look?

    Correct answer: Box A (where she last saw it)
    This requires understanding that others have false beliefs.
    """

    model = BrainSystem()

    # Present story
    story = """
    Sally has a marble. She puts it in Box A.
    Sally leaves the room.
    Anne moves the marble from Box A to Box B.
    Sally returns.
    """

    model.read_story(story)

    # Question: Where will Sally look?
    prediction = model.answer_question("Where will Sally look for her marble?")

    assert 'A' in prediction or 'original' in prediction.lower(), \
        "Failed false belief test"
    print(f"✓ False belief test passed: {prediction}")

    # Harder variant
    harder_story = """
    John puts a cookie in the cupboard.
    He goes outside.
    Mary moves the cookie to the drawer.
    John comes back in.
    """

    prediction2 = model.answer_question("Where will John first look?")
    assert 'cupboard' in prediction2.lower(), "Failed harder false belief"
    print(f"✓ Harder false belief test passed: {prediction2}")
```

**Success Criterion:** >80% accuracy on false belief tasks.

---

### Test 4.2: Planning Depth

**What we're measuring:** Can the system plan multi-step sequences?

```python
def test_planning_depth():
    """
    Give goals requiring multiple steps.
    Measure: how deep can it plan?
    """

    model = BrainSystem()

    # Task: "Get a drink of water in a room where
    # - Glass is on shelf
    # - Water is in pitcher
    # - You need to reach shelf first"

    test_cases = [
        {
            'goal': 'drink_water',
            'obstacles': ['shelf_high', 'pitcher_full'],
            'steps': ['find_chair', 'climb_chair', 'get_glass', 'get_pitcher', 'pour', 'drink'],
            'min_depth': 6
        },
        {
            'goal': 'make_sandwich',
            'obstacles': ['bread_in_cupboard', 'jam_in_fridge'],
            'steps': ['get_bread', 'get_jam', 'get_knife', 'spread', 'close'],
            'min_depth': 5
        },
    ]

    success_count = 0
    for tc in test_cases:
        # Can the model plan required steps?
        plan = model.plan(tc['goal'], tc['obstacles'])

        # Check: does plan include necessary steps?
        plan_completeness = sum(1 for step in tc['steps'] if step in plan) / len(tc['steps'])

        if plan_completeness > 0.8 and len(plan) >= tc['min_depth']:
            success_count += 1

    success_rate = success_count / len(test_cases)
    assert success_rate > 0.7, "Planning depth insufficient"
    print(f"✓ Planning test: {success_rate:.1%} success on multi-step tasks")
```

**Success Criterion:** >70% success on 5+ step planning tasks.

---

## 🧪 Stage 5 Tests: Preschooler (Years 2-4)

### Test 5.1: Reading Comprehension

**What we're measuring:** Can it read text and answer questions?

```python
def test_reading_comprehension():
    """
    Standard reading comprehension benchmark.
    Present passage, ask questions, measure accuracy.
    """

    model = BrainSystem()

    # Use standard dataset (e.g., SQuAD-style)
    passages = load_reading_comprehension_dataset()

    accuracy_by_type = {}
    for passage_type in ['factual', 'inferential', 'vocabulary']:
        correct = 0
        total = 0

        for passage, questions in passages[passage_type]:
            model.read_passage(passage)

            for question, answer in questions:
                predicted = model.answer_question(question)

                if predicted_matches_answer(predicted, answer):
                    correct += 1
                total += 1

        accuracy = correct / total
        accuracy_by_type[passage_type] = accuracy
        print(f"  {passage_type}: {accuracy:.1%}")

    overall = mean(accuracy_by_type.values())
    assert overall > 0.6, "Reading comprehension too low"
    print(f"✓ Reading comprehension: {overall:.1%} overall")
    return accuracy_by_type
```

**Success Criterion:** >60% accuracy on reading comprehension.

---

### Test 5.2: Logical Reasoning

**What we're measuring:** Can it reason logically?

```python
def test_logical_reasoning():
    """
    Test logical inference:
    - Syllogisms
    - Modus ponens/tollens
    - Conditional reasoning
    """

    model = BrainSystem()

    logic_problems = [
        {
            'premise': "All dogs are animals. Fido is a dog.",
            'question': "Is Fido an animal?",
            'answer': "yes"
        },
        {
            'premise': "If it rains, the ground is wet. The ground is not wet.",
            'question': "Did it rain?",
            'answer': "no"
        },
        {
            'premise': "Some birds fly. All sparrows are birds.",
            'question': "Do all sparrows fly?",
            'answer': "maybe"  # Correct: we don't know
        },
    ]

    correct = 0
    for problem in logic_problems:
        model.read_premise(problem['premise'])
        answer = model.answer_question(problem['question'])

        if answer.lower() == problem['answer'].lower():
            correct += 1

    accuracy = correct / len(logic_problems)
    assert accuracy > 0.7, "Logical reasoning insufficient"
    print(f"✓ Logical reasoning: {accuracy:.1%} accuracy")
```

**Success Criterion:** >70% accuracy on logical reasoning.

---

## 📊 Continuous Metrics (All Stages)

### Learning Curve

```python
def plot_learning_curves():
    """
    For every test, plot learning curve over time.
    Expected: mostly smooth improvement with noise.
    """

    # On any task:
    performance_over_time = []

    for epoch in range(num_epochs):
        perf = evaluate(test_set)
        performance_over_time.append(perf)

        # Plot
        plt.plot(performance_over_time)
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.title('Learning Curve')
        plt.show()

    # Check: monotonic improvement?
    early = mean(performance_over_time[:10])
    late = mean(performance_over_time[-10:])
    improvement_rate = (late - early) / early

    return improvement_rate  # Should be >0
```

### Generalization Gap

```python
def measure_generalization():
    """
    Train loss vs validation loss.
    Healthy: both decrease, not too far apart.
    Bad: train loss down, validation flat or up.
    """

    train_loss = []
    val_loss = []

    for epoch in range(num_epochs):
        train_loss.append(evaluate_on_train())
        val_loss.append(evaluate_on_validation())

    # Plot
    plt.plot(train_loss, label='train')
    plt.plot(val_loss, label='validation')
    plt.legend()
    plt.show()

    # Check: generalization gap reasonable?
    gap = val_loss[-1] - train_loss[-1]
    assert gap < 0.2, "Overfitting detected"
```

### Transfer Learning

```python
def measure_transfer():
    """
    Train on Task A, then test on Task B.
    How much faster does it learn Task B?
    """

    # Training on Task A
    model = BrainSystem()
    epochs_to_convergence_A = train_until_convergence(model, task_A)

    # Now add Task B
    epochs_to_convergence_B = train_until_convergence(model, task_B)

    # Compare to model trained on B from scratch
    fresh_model = BrainSystem()
    epochs_fresh_B = train_until_convergence(fresh_model, task_B)

    transfer_speedup = epochs_fresh_B / epochs_to_convergence_B

    print(f"Transfer speedup: {transfer_speedup:.1f}×")
    assert transfer_speedup > 1.5, "Transfer learning not working"
```

---

## 🎯 Overall Dashboard

```python
def create_development_dashboard():
    """
    Central place to see how the brain is developing.
    """

    tests = {
        'Stage 1: Newborn': [
            test_prediction_improvement(),
            test_representation_structure(),
        ],
        'Stage 2: Infant': [
            test_associative_learning(),
            test_novelty_preference(),
        ],
        'Stage 3: Growing Infant': [
            test_word_segmentation(),
            test_novel_word_generalization(),
        ],
        'Stage 4: Toddler': [
            test_false_belief_understanding(),
            test_planning_depth(),
        ],
        'Stage 5: Preschooler': [
            test_reading_comprehension(),
            test_logical_reasoning(),
        ],
    }

    # Visualization
    for stage, stage_tests in tests.items():
        print(f"\n{stage}")
        for test_result in stage_tests:
            status = "✓" if test_result['passed'] else "✗"
            print(f"  {status} {test_result['name']}: {test_result['score']:.1%}")

    return tests
```

---

## ✅ Summary

**This framework lets you:**
- ✅ Verify the system is actually learning
- ✅ Measure learning speed (efficiency)
- ✅ Detect when something is broken
- ✅ Track development stages
- ✅ Compare to biological benchmarks

**Key insight:** If it passes these tests in order, you've built something that learns like a baby.

If it doesn't, you can pinpoint which learning mechanism is broken.

This is your validation pipeline.
