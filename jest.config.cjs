module.exports = {
  projects: [
    {
      displayName: 'backend-bdd',
      testEnvironment: 'node',
      testMatch: ['<rootDir>/tests/**/*.steps.ts'],
      transform: {
        '^.+\\.ts$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.json' }],
      },
      moduleFileExtensions: ['ts', 'js', 'json'],
    },
    {
      displayName: 'frontend-deliverer',
      testEnvironment: 'jsdom',
      testMatch: ['<rootDir>/frontend/src/**/*.test.ts', '<rootDir>/frontend/src/**/*.test.tsx'],
      setupFilesAfterEnv: ['<rootDir>/frontend/jest.setup.ts'],
      transform: {
        '^.+\\.(ts|tsx)$': ['ts-jest', { tsconfig: '<rootDir>/tsconfig.json' }],
      },
      moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
    },
  ],
}