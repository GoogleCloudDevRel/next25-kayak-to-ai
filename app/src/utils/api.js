import { useKayakStore } from "@/store";
import { deferred } from "./deferred";

const locationNames = [
  "Lake Union",
  "Green Lake",
  "Seward Park",
  "Matthews Beach Park",
  "Lake Sammamish"
];

let sendPromptPromise = null;

export const sendPrompt = async () => {
  if (sendPromptPromise) {
    return sendPromptPromise;
  }

  const { prompt } = useKayakStore();

  console.log("prompt", prompt);

  if (!prompt) return;

  const defer = deferred();
  sendPromptPromise = defer;

  // TODO: implement this
  // fetch(...)

  await new Promise((resolve) => setTimeout(resolve, 1000));

  const locationName = locationNames[Math.floor(Math.random() * locationNames.length)];

  useKayakStore().setLocation({
    name: locationName,
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.<br><br>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    image: "/images/kayak/image-grid-1.jpg",
  });

  sendPromptPromise.resolve();
  sendPromptPromise = null;
}

let moveKayakAndGetCodePromise = null;
export const moveKayakAndGetCode = async () => {
  if (moveKayakAndGetCodePromise) {
    return moveKayakAndGetCodePromise;
  }

  const defer = deferred();
  moveKayakAndGetCodePromise = defer;

  useKayakStore().setIsMoving(true)

  // TODO: call API to move kayak
  // fetch(...)

  // TODO: call API to get code
  // fetch(...)

  await new Promise((resolve) => setTimeout(resolve, 1000));

  const code = /*python */ `
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
print(f"Even numbers: {even_numbers}")`

  useKayakStore().setCode(code)

  moveKayakAndGetCodePromise.resolve();
  moveKayakAndGetCodePromise = null;
}

let isKayakArrivedPromise = null;
export const checkIfKayakArrived = async () => {

  if (isKayakArrivedPromise) {
    return isKayakArrivedPromise;
  }

  const defer = deferred();
  isKayakArrivedPromise = defer;

  let interval = null;
  let debugMaxTries = 4;
  let debugTries = 0;

  // create a polling function that checks if the kayak has arrived
  const isKayakArrived = () => {
    // TODO: implement this
    // fetch(...)
    // if (/* kayak has arrived */) {

    if (debugTries >= debugMaxTries) {
      clearInterval(interval);
      useKayakStore().setArrived(true);
      isKayakArrivedPromise.resolve(true);
      isKayakArrivedPromise = null;
      return;
    }

    debugTries++;
    console.log("debugTries", debugTries);
  }

  interval = setInterval(isKayakArrived, 1000);

  await new Promise((resolve) => setTimeout(resolve, 1000));
}
