# Translations

To make our app available globally, we use Django's localization and internationalization features. These are stored in this folder sorted by language.

`.po` files are text files used to manage translations in software projects, especially in Django projects. The structure of a `.po` file is standardized and includes certain structural and formatting elements to manage translations of texts and messages. Here is a brief explanation of the structure of a `.po` file:

## Basic structure of a `.po` file

1. **Header comments**

- **File header:** Contains meta information about the file, such as the language used for the translations and the name of the project.
- **Example:**

```plaintext
# This file is distributed under the same license as the PACKAGE package.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Language: en\n"
```

2. **Messages and translations**

- **`msgid` (original message):** The original text to be translated.
- **`msgstr` (translation):** The translation of the `msgid`.

- **Example:**

```plaintext
msgid "Welcome"
msgstr "Welcome"
```

3. **Comments**

- **Comments for translators:** Comments that help translators better understand the context of the `msgid`.
- **Reference comments:** References to the source code to show the origin of the message (e.g. file name and line number).
- **Example:**

```plaintext
# Translators: Greeting message on the homepage
msgid "Welcome"
msgstr "Welcome"

#: views.py:42
msgid "Error: Invalid input"
msgstr "Error: Invalid input"
```

4. **Fuzzy flag**

- **Fuzzy flag:** Flags translations that may be out of date or uncertain. This is often used as a placeholder to indicate possible changes.
- **Example:**

```plaintext
#| msgid "Old message"
#| msgstr "Old message"
```

5. **Context**

- **msgctxt (context):** An optional line that provides additional context to a `msgid` to avoid ambiguity.
- **Example:**

```plaintext
msgctxt "button"
msgid "Submit"
msgstr "Submit"
```

## Conventions

Please follow the following conventions to secure readability and maintainability:

- **Write in the appropriate section**: Sections are marked by the `# SECTION` comment.
  - `SENTENCES_STD`: This section includes standard sentences used across the application, such as common phrases or dialogue.
  - `SHORTS_STD`: This section contains short, standard texts like labels and buttons (max 3 words).
  - `BODY_TEXT_STD`: This section holds longer blocks of standard text, such as paragraphs or descriptions.
  - `ERROR_STD`: This section includes standard error messages that are used throughout the application.
  - `SENTENCES_FORMAT`: This section is for sentences with specific formatting or placeholders.
  - `SHORTS_FORMAT`: This section contains short texts with formatting or placeholders.
  - `BODY_TEXT_FORMAT`: This section includes longer blocks of text with formatting or placeholders.
  - `ERROR_FORMAT`: This section contains error messages that include formatting or placeholders.
- **Use reference comments**: to explain relations with the source code
- **Use the fuzzy flag**: For values that don't have to be translated (yet)
- **Add context**: for non-self-explanatory values
