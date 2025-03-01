import TextGeneric from '@/components/TextGeneric.vue'
import { ref } from 'vue'
import './TextGeneric.stories.scss'

const Template = (args) => ({
  components: { TextGeneric },
  setup() {
    const textGenericWords = ref(null)
    const triggerAnimateIn = () => {
      textGenericWords.value.animateIn()
    }
    const triggerAnimateSet = () => {
      textGenericWords.value.animateSet()
    }
    return { args, textGenericWords, triggerAnimateIn, triggerAnimateSet }
  },
  template: /* html */ `
    <div class="text-container">
      <TextGeneric ref="textGenericWords" v-bind="args" />
      <button class="animate-in-button" @click="triggerAnimateIn">Animate In</button>
      <button class="animate-set-button" @click="triggerAnimateSet">Animate Set</button>
    </div>
  `,
})

export const Primary = Template.bind({})
Primary.args = {
  text: 'Hello this is a text component',
  type: 'words',
}

export default {
  title: 'Components/TextGeneric',
  component: TextGeneric,
  parameters: {
    layout: 'centered',
  },
}
