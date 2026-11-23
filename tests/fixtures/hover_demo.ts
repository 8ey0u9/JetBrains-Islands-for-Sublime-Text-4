/**
 * Build a greeting / 生成问候语。
 *
 * @param name The person to greet. 支持中文。
 * @param repeat Number of repetitions, default 1.
 * @returns A greeting string.
 * @example
 * ```ts
 * greet("Islands", 2);
 * ```
 * @see https://www.typescriptlang.org/docs/
 */
export function greet(name: string, repeat: number = 1): string {
    return Array(repeat).fill(`Hello, ${name}!`).join(" ");
}

const message = greet("Islands", 2);
const broken = greet(123); // Intentional diagnostic; preserve native Quick Fix.
console.log(message, broken);
console.log(mesage); // Intentional spelling error for server-provided Quick Fix.
