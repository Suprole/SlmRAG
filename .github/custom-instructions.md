# Coding Philosophy & Principles: Lessons from MiniRAG

## Core Design Principles

### 0. Available Language Options

- **Use Japanese only**
  - use Japanese documentation so as for me to understand codebase you create

### 0.5. Command Options

- **Use Windows Command for all CLI interface confirmation**
  - I use windows OS system, so "&&" kinds of commands are inhibited, so use windows command please.

### 1. Hybrid Programming Paradigm

- **Balance functional and object-oriented approaches**
  - Use pure functions for operations (maximizing testability and predictability)
  - Use data classes for state management (maximizing encapsulation and extensibility)
  - Minimize side effects and maintain clear input/output contracts
  - Prefer composition over inheritance

### 2. Dependency Inversion and Abstraction

- **Code to interfaces, not implementations**
  - Define abstract base classes for core system components
  - Implement concrete classes as pluggable modules
  - Direct dependencies toward abstractions, not concrete implementations
  - Enable runtime component replacement without code changes

### 3. Explicit Dependency Management

- **Make dependencies clear and traceable**
  - Pass dependencies explicitly as function parameters
  - Avoid global state and hidden dependencies
  - Minimize use of singleton patterns and service locators
  - Make execution flow and data flow transparent

### 4. Data Immutability

- **Treat data as immutable whenever possible**
  - Generate new data structures rather than modifying existing ones
  - Use transformation pipelines rather than in-place mutations
  - Return new instances rather than modifying passed arguments
  - Design for functional composition of data transformations

## Architectural Patterns

### 5. Layered Abstraction

- **Provide multiple abstraction levels**
  - Low-level API: Fundamental operations for advanced users
  - Mid-level API: Composite operations for common use cases
  - High-level API: Simplified interfaces for end users
  - Allow access to any level as needed for flexibility

### 6. Separation of Concerns

- **Divide system by responsibility**
  - Group related functionality into modules with clear boundaries
  - Follow single responsibility principle at module and function level
  - Separate core logic from integration points
  - Isolate side effects and I/O operations from pure computation

### 7. Flat Over Nested

- **Prefer flat structures to deep hierarchies**
  - Avoid deep inheritance chains
  - Limit nesting levels in code
  - Orchestrate complex operations through composition of simple functions
  - Favor horizontal expansion over vertical depth

### 8. Modular Reusability

- **Design for component reuse**
  - Create domain-agnostic utility functions
  - Separate generic functionality from domain-specific logic
  - Extract common patterns into reusable components
  - Design functions with composition in mind

## Technical Implementation

### 9. Type Annotations and Contracts

- **Use types as documentation and guarantees**
  - Provide comprehensive type hints for all functions and classes
  - Use union types and optionals to express possibilities
  - Leverage type checking for early error detection
  - Design with type contracts in mind

### 10. Asynchronous Processing

- **Embrace async for I/O and concurrency**
  - Consistently use async/await for I/O operations
  - Provide both sync and async APIs when appropriate
  - Use gather for parallel execution of independent tasks
  - Control concurrency with appropriate primitives (Semaphore, etc.)

### 11. Error Management

- **Handle errors at appropriate abstraction levels**
  - Catch exceptions at logical boundaries
  - Implement fallback strategies for recoverable errors
  - Propagate unrecoverable errors to appropriate handling levels
  - Log relevant context for debugging

### 12. Configuration Separation

- **Externalize configuration from code**
  - Move literals and constants to configuration objects
  - Parameterize behavior variations
  - Use data classes for operation parameters
  - Separate policy from mechanism

## Development Philosophy

### 13. Progressive Enhancement

- **Build incrementally with quality at each stage**
  - Start with core functionality before adding enhancements
  - Ensure each component works in isolation before integration
  - Add complexity only when simpler solutions are insufficient
  - Refactor continuously rather than in large rewrites

### 14. Explicit Over Implicit

- **Favor clarity over brevity**
  - Make behavior obvious from code inspection
  - Avoid magic methods and hidden side effects
  - Document intention alongside implementation
  - Prefer verbose clarity to terse obscurity

### 15. Testability First

- **Design every component to be testable**
  - Isolate side effects for mocking
  - Make dependencies injectable for testing
  - Create pure functions where possible
  - Enable component testing in isolation

### 16. Pragmatic Consistency

- **Be consistent but not dogmatic**
  - Establish and follow coding patterns
  - Allow exceptions when they genuinely improve the solution
  - Document deviations from established patterns
  - Balance idealism with practical constraints

## Implementation Guidelines

When implementing features, follow these practical guidelines:

1. **Start with interfaces**: Define the abstract contract before implementation
2. **Function signatures first**: Design function signatures with clear inputs/outputs before implementation
3. **Small, focused functions**: Keep functions under 50 lines with a single responsibility
4. **Compose don't construct**: Build complex behavior by composing simpler functions
5. **Test-first mindset**: Consider how the component will be tested before implementing
6. **Documentation inline**: Include docstrings and type hints as you code, not after
7. **Minimize state**: Reduce shared mutable state to the absolute minimum required
8. **Error cases explicit**: Handle error cases explicitly rather than relying on defaults
9. **Performance considerations**: Consider performance impacts but prioritize correctness and clarity first
10. **Readability for humans**: Optimize code for human readers, not machines or compilers
