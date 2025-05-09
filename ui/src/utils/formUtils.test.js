import { describe, expect, it } from '@jest/globals';

import { shouldUseTextarea } from './formUtils';

describe('shouldUseTextarea', () => {
  it('returns true if value contains a newline', () => {
    expect(shouldUseTextarea('hello\nworld')).toBe(true);
  });
  it('returns false if value does not contain a newline', () => {
    expect(shouldUseTextarea('hello world')).toBe(false);
  });
  it('returns false if value is null, a number, or an object', () => {
    expect(shouldUseTextarea(null)).toBe(false);
    expect(shouldUseTextarea(123)).toBe(false);
    expect(shouldUseTextarea({})).toBe(false);
  });
});
