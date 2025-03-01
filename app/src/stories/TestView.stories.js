import TestView from '@/components/TestView.vue'
import './TestView.stories.scss'

const Template = (args) => ({
  components: { TestView },
  setup() {
    return { args }
  },
  template: /* html */ `
    <TestView v-bind="args" />
  `,
})

export const Primary = Template.bind({})
Primary.args = {
}

export const Secondary = Template.bind({})
Secondary.args = {
}

export default {
  title: 'Components/TestView',
  component: TestView,
  parameters: {
    layout: 'centered',
  },
}
