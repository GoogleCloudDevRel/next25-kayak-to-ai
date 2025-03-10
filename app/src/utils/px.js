export function pxToVw(value, base = 1920) {
  return (value / base) * 100 + 'vw'
}

export function pxToVh(value, base = 1080) {
  return (value / base) * 100 + 'vh'
}
