<template>
  <div
    class="codeblock"
    ref="codeBlockRef"
  >
    <div class="codeblock__title">
      <TitleWithIcon
        ref="titleRef"
        icon="gemini"
        textVariant="bold-24"
        title="Code Execution"
      />
    </div>
    <pre class="line-numbers"><code ref="codeRef" /></pre>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import Prism from '@/utils/prism'
import gsap from 'gsap'
import TitleWithIcon from './TitleWithIcon.vue'
import { pxToVw4k } from '@/utils/px'

const props = defineProps({
  language: {
    type: String,
    default: 'python',
  },
  codeSnippet: {
    type: String,
    default: '',
  },
  isTv: {
    type: Boolean,
    default: false,
  },
})

const codeClass = `language-${props.language}`

const codeBlockRef = ref(null)
const titleRef = ref(null)
const codeRef = ref(null)

// Re-highlight when code changes
watch(
  () => props.codeSnippet,
  async () => {
    if (!codeRef.value || !props.codeSnippet) return

    if (!codeRef.value.classList.contains(codeClass)) {
      codeRef.value.classList.add(codeClass)
    }

    gsap.to(codeRef.value, {
      text: {
        value: props.codeSnippet,
        preserveSpaces: true,
        speed: 8,
      },
      duration: 2,
      ease: 'none',
      onUpdate: () => {
        Prism.highlightElement(codeRef.value)
      },
    })
  },
)

const animateIn = (delay = 0) => {
  gsap.to(codeBlockRef.value, {
    x: 0,
    delay,
    duration: 1,
    ease: 'power4.out',
    onStart: () => {
      gsap.set(codeBlockRef.value, {
        pointerEvents: 'auto',
      })
      titleRef.value.animateIn()
    },
  })
}

const animateOut = () => {
  gsap.to(codeBlockRef.value, {
    x: props.isTv ? codeBlockRef.value.offsetWidth + pxToVw4k(144) : '100%',
    duration: 1,
    ease: 'power4.out',
  })
  titleRef.value.animateOut()
}

const animateSet = async () => {
  await Promise.all([
    gsap.set(codeBlockRef.value, {
      x: props.isTv ? codeBlockRef.value.offsetWidth + pxToVw4k(144) : '100%',
    }),
    titleRef.value.prepare(),
  ])
}

defineExpose({
  animateIn,
  animateOut,
  animateSet,
})
</script>

<style lang="scss">
.codeblock {
  height: 100%;

  &__title {
    height: 54px;
    margin-bottom: px-to-vw(32);
    display: flex;
    justify-content: flex-start;
    align-items: center;
    svg {
      max-width: 80%;
      color: $lightGreen;
    }
  }

  border-radius: px-to-vw(32);
  border-bottom-right-radius: 0;
  border-top-right-radius: 0;
  padding: px-to-vw(48);
  position: relative;
  width: 100%;
  margin: 0 auto;
  overflow: hidden;
  background: rgba(38, 53, 47, 0.35);
  backdrop-filter: blur(10px);
  color: white;

  &:before {
    border-radius: px-to-vw(32);
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;
    z-index: -1;
  }

  @include gradient-border((45deg, rgba(120, 122, 121, 0.35), rgba(38, 53, 47, 0.35)), 1px);

  pre {
    border-top: 1px solid rgba(38, 53, 47, 0.35);
    margin: 0 !important;
    padding: 0 !important;
    padding-top: px-to-vw(40) !important;
    overflow-x: hidden;
    word-wrap: break-word;
    white-space: pre !important; // Force preserve whitespace
    background: none;
    overflow-y: scroll;
    height: 100%;
    &::-webkit-scrollbar {
      display: none;
    }
  }

  code {
    margin: 0 !important;
    padding: 0 !important;
    font-size: px-to-vw(18);
    line-height: 1.5;
    display: block;
    // white-space: pre !important; // Force preserve whitespace
    word-wrap: break-word;
    tab-size: 4;
    span {
      white-space: normal !important; // Force preserve whitespace
    }

    .line-wrapper {
      --line-mask: 0;
      --text-opacity: 0;
      --line-mask-origin: center left;
      display: inline-block;
      position: relative;
      line-height: 1.2;
      overflow: hidden;
      border-radius: 3px;

      &::before {
        content: '';
        position: absolute;
        top: calc(50%);
        transform-origin: var(--line-mask-origin);
        transform: translateY(-50%) scaleX(var(--line-mask));
        left: 0;
        width: 100%;
        height: calc(100% + 1px);
        background: linear-gradient(270deg, #123a1d, #34a853 65.38%);
        background-size: 400% 400%;
        animation: gradient 10s linear infinite;
        z-index: 1;
      }

      &:nth-child(odd) {
        &::before {
          background: linear-gradient(-270deg, #206b34, #34a853 65.38%);
        }
      }

      @keyframes gradient {
        0% {
          background-position: 0% 50%;
        }
        50% {
          background-position: 100% 50%;
        }
        100% {
          background-position: 0% 50%;
        }
      }
      .line-text {
        opacity: var(--text-opacity);
      }
    }
  }

  /*
  Name: Duotone Sea
  Author: by Simurai, adapted from DuoTone themes by Simurai for Atom (http://simurai.com/projects/2016/01/01/duotone-themes)

  Conversion: Bram de Haan (http://atelierbram.github.io/Base2Tone-prism/output/prism/prism-base2tone-sea-dark.css)
  Generated with Base16 Builder (https://github.com/base16-builder/base16-builder)
  */
  code[class*='language-'],
  pre[class*='language-'] {
    font-family:
      Consolas, Menlo, Monaco, 'Andale Mono WT', 'Andale Mono', 'Lucida Console',
      'Lucida Sans Typewriter', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Liberation Mono',
      'Nimbus Mono L', 'Courier New', Courier, monospace;
    // @include fluid(
    //   'font-size',
    //   (
    //     xxl: 18px,
    //     fourk: 32px,
    //   )
    // );
    line-height: 1.375;
    direction: ltr;
    text-align: left;
    white-space: pre;
    word-spacing: normal;
    word-break: normal;

    -moz-tab-size: 4;
    -o-tab-size: 4;
    tab-size: 4;

    -webkit-hyphens: none;
    -moz-hyphens: none;
    -ms-hyphens: none;
    hyphens: none;
    //background: #1d262f;
    color: #57718e;
    text-shadow: none !important;
  }

  pre[class*='language-']::-moz-selection,
  pre[class*='language-'] ::-moz-selection,
  code[class*='language-']::-moz-selection,
  code[class*='language-'] ::-moz-selection {
    text-shadow: none;
    background: #004a9e;
  }

  pre[class*='language-']::selection,
  pre[class*='language-'] ::selection,
  code[class*='language-']::selection,
  code[class*='language-'] ::selection {
    text-shadow: none;
    background: #004a9e;
  }

  /* Code blocks */
  pre[class*='language-'] {
    padding: 1em;
    margin: 0.5em 0;
    overflow: auto;
  }

  /* Inline code */
  :not(pre) > code[class*='language-'] {
    padding: 0.1em;
    border-radius: 0.3em;
  }

  .token.comment,
  .token.prolog,
  .token.doctype,
  .token.cdata {
    color: #4a5f78;
  }

  .token.punctuation {
    color: #4a5f78;
  }

  .token.namespace {
    opacity: 0.7;
  }

  .token.tag,
  .token.operator,
  .token.number {
    color: #0aa370;
    background: none;
  }

  .token.property,
  .token.function {
    color: #57718e;
  }

  .token.tag-id,
  .token.selector,
  .token.atrule-id {
    color: #ebf4ff;
  }

  code.language-javascript,
  .token.attr-name {
    color: #7eb6f6;
  }

  code.language-css,
  code.language-scss,
  .token.boolean,
  .token.string,
  .token.entity,
  .token.url,
  .language-css .token.string,
  .language-scss .token.string,
  .style .token.string,
  .token.attr-value,
  .token.keyword,
  .token.control,
  .token.directive,
  .token.unit,
  .token.statement,
  .token.regex,
  .token.atrule {
    color: #47ebb4;
  }

  .token.placeholder,
  .token.variable {
    color: #47ebb4;
  }

  .token.deleted {
    text-decoration: line-through;
  }

  .token.inserted {
    border-bottom: 1px dotted #ebf4ff;
    text-decoration: none;
  }

  .token.italic {
    font-style: italic;
  }

  .token.important,
  .token.bold {
    font-weight: bold;
  }

  .token.important {
    color: #7eb6f6;
  }

  .token.entity {
    cursor: help;
  }

  pre > code.highlight {
    outline: 0.4em solid #34659d;
    outline-offset: 0.4em;
  }

  /* overrides color-values for the Line Numbers plugin
  * http://prismjs.com/plugins/line-numbers/
  */
  .line-numbers.line-numbers .line-numbers-rows {
    border-right-color: #1f2932;
  }

  .line-numbers .line-numbers-rows > span:before {
    color: #2c3847;
  }

  /* overrides color-values for the Line Highlight plugin
  * http://prismjs.com/plugins/line-highlight/
  */
  .line-highlight.line-highlight {
    background: rgba(10, 163, 112, 0.2);
    background: -webkit-linear-gradient(left, rgba(10, 163, 112, 0.2) 70%, rgba(10, 163, 112, 0));
    background: linear-gradient(to right, rgba(10, 163, 112, 0.2) 70%, rgba(10, 163, 112, 0));
  }
}
</style>
