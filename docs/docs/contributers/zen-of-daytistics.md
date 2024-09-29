# Zen of Daytistics
We could fill this guide with endless rules, but let's be honest—no one will remember them all. The key is to focus on **a few core principles**: write **clean code**, keep it **simple**, and **test thoroughly**. By sticking to these basics, we ensure contributions are both effective and maintainable without overwhelming contributors with unnecessary complexity.

### **I. Who Does Format Code By Hand?**
- Use **Prettier** for JavaScript and **Black** for Python. For Zig, use the `zig fmt` command. Don't waste time formatting code by hand.

### **II. Keep It Simple**
- Simplicity wins. Avoid over-engineering and keep the logic easy to follow. 


### **III. Write Atomic Commits**
- Keep commits **small** and **focused** on a single task. Write **clear commit messages** that explain the changes made.

### **IV. Test Everything**
- Add **unit tests** for each function, and **integration tests** for entire workflows. Ensure code is **test-driven**.

### **V. Use OOP Wisely**
- Favor **composition over inheritance**. Keep classes **small** and **focused** on one responsibility.

### **VI. Error Handling**
- Always handle errors gracefully using Python’s **try-except**, JavaScript’s **try-catch**, and **Zig’s error-handling**.

### **VII. Respect our Vue Components**
- Always build Vue components so that each part of the script handles a variable or an object. First come props and emits, then the named objects and finally `watch` and lifecycle hooks.

### **VIII. Consistent Naming**
- Use meaningful, descriptive names for variables, functions, and classes. Stick to consistent naming conventions across all languages.

### **IX. Modularize Code**
- Break code into **reusable components**. Each module, function, or class should have a clear, specific responsibility.

### **X. Document Your Code**
- Because we do not use an external documentation tool, **write clear comments** in your code. Explain the purpose of each function, class, and module.