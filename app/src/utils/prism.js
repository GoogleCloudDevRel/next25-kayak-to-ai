import Prism from "prismjs";

import "prismjs/components/prism-python";
import "prismjs/themes/prism.css"; // You can choose different themes
import "prismjs/plugins/line-numbers/prism-line-numbers";

Prism.hooks.add("after-highlight", function (env) {
  const code = env.element.innerHTML.split("\n");
  env.element.innerHTML = code
    .map(
      (line, index) =>
        /* html */ `<span class="line-wrapper" data-line="${index + 1}"><span class="line-text">${line}</span></span>`
    )
    .join("\n");
});

export default Prism;
