declare module 'typewriter-effect/dist/core' {
    export default class Typewriter {
      constructor(element: HTMLElement, options?: any);
      typeString(str: string): Typewriter;
      pauseFor(ms: number): Typewriter;
      deleteAll(): Typewriter;
      start(): void;
    }
  }
  