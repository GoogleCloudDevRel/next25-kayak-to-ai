import { gsap } from "gsap";
import { Flip } from "gsap/Flip";
import { TextPlugin } from "gsap/TextPlugin";
import { deferred } from "./deferred";

gsap.registerPlugin(Flip);
gsap.registerPlugin(TextPlugin);

export const waitUntil = async (condition, checkTime = 1 / 60) => {
  let result = deferred();

  function check() {
    if (condition()) {
      result.resolve();
    } else {
      gsap.delayedCall(checkTime, check);
    }
  }

  check();

  return result;
}

export * from "gsap";
export { Flip };
