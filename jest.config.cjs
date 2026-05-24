module.exports = {
  testEnvironment: 'node',
  testMatch: ['<rootDir>/tests/**/*.steps.ts'],
  transform: {
    '^.+\\.ts$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.json' }],
  },
  moduleFileExtensions: ['ts', 'js', 'json'],
}