import { defineStore } from "pinia";

export const useKayakStore = defineStore('kayak', {
  state: () => ({
    isMoving: false,
    isArrived: false,
    prompt: 'Prompt selected previously',
    code: /*python */ `
# Example 1: List comprehension and string manipulation
names = ['alice', 'bob', 'charlie']
capitalized = [name.title() for name in names]
print(f"Capitalized names: {capitalized}")

# Example 2: Working with dictionaries
student_scores = {
    'Alice': 95,
    'Bob': 87,
    'Charlie': 92
}
avg_score = sum(student_scores.values()) / len(student_scores)
print(f"Average score: {avg_score:.2f}")

# Example 3: Using lambda and filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")`,
  }),
  actions: {
    setIsMoving(isMoving) {
      this.isMoving = isMoving
    },
    setPrompt(prompt) {
      this.prompt = prompt
      this.isMoving = false
      this.isArrived = false
    },
    setArrived(isArrived) {
      this.isArrived = isArrived
    },
    reset() {
      this.isMoving = false
      this.isArrived = false
      this.prompt = 'Prompt selected previously'
    },
  },
})
