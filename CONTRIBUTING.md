# Contributing to Daytistics

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)
- [Join The Project Team](#join-the-project-team)

## Code of Conduct

This project and everyone participating in it is governed by the
[Daytistics Code of Conduct](./CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <gall.dev@proton.me>.

## I Have a Question

If you have any questions you can post them in the [discussions](https://github.com/adf-web/daytistics/discussions/categories/questions).

## I Want To Contribute

> ### Legal Notice
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Your first code contribution

Before you can contribute to the project, find an issue that you want to work on and write under it that you are working on it.<br><br>
After you have found your issue, please follow the following workflow and integrate the code change:

1. Fork the project repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your code changes.
4. Make your code changes and commit them to your branch.
5. Push your branch to your forked repository on GitHub.
6. Open a pull request to submit your code changes for review.

If you are new to working with Github, we recommend [this tutorial](https://www.youtube.com/watch?v=RGOj5yH7evk&t=425s).
<br><br>
Please make sure to follow the project's coding style guidelines and provide clear documentation for your changes. We appreciate your contribution and look forward to reviewing your code!

### Reporting Bugs

#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions. If you are looking for support, you might want to check [this section](https://github.com/adf-web/daytistics/discussions/categories/questions).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/adf-web/daytistics/issues?q=is%3Aopen+is%3Aissue+label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to <gall.dev@proton.me>.

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/adf-web/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the _reproduction steps_ that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The core team will label the issue accordingly.
- A core team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs repro`.
- If the team is able to reproduce the issue, it will be marked `needs fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

<!-- You might want to create an issue template for bugs and errors that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Daytistics, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation]() carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/adf-web/daytistics-core/discussions/categories/ideas) to see if the enhancement has already been suggested. If it has, add a comment to the existing discussion instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset.

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub discussions](https://github.com/adf-web/daytistics-core/discussions/categories/ideas).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots and animated GIFs** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
- **Explain why this enhancement would be useful** to most Daytistics users. You may also want to point out the other projects that solved it better and which could serve as inspiration.
  <br><br>

  After you have contributed your enhancement, the enhancement will be evaluated by our team. If it is accepted by the team, an issue will be created for it. For major changes, community votes will also be held.

### Project Structure

- **`accounts`**: User editing & Allauth overrides
- **`activities`**: Creating and editing activities
- _**`feelings`**: Creating and editing feelings_
- **`config`**: Django project base
- _**`analyses`**: Statistical analyses and visualizations by Daytistics_
- **`daytistics`**: Creating and editing daytistics
- **`home`**: Pages that do not require login
- **`templates/pages`**: Template pages (consisting of components)
- **`templates/components`**: Components for pages
- **`tests`**: Tests written in PyTest

If a folder is _italicized_, it is not yet integrated.

### Other Ways to Contribute

You're not a great developer or you just don't feel like contributing code? No problem! You can also get involved in other ways by helping us with the design. Just take a look at [this repository](https://github.com/adf-web/daytistics-assets/issues).

## Styleguides

### Commit Messages

- **Formulate clearly and concisely**: The commit name should be a maximum of 50 characters long and precise.
- **Use the imperative form**: Write the commit message as if you were giving commands.
- **One commit, one change**: Keep your commits small and thematically consistent. A commit should only do one thing, e.g. a bug fix or a new feature.
- **Provide relevant details**: If necessary, add more details, such as why the change was made or what impact it has.
- **References to tickets or issues**: Reference the issue ID if given
- **Avoid general statements**: Messages like "Update", "Fix bugs" or "Minor changes" are not meaningful. Be specific!
- **One sentence per commit**: Use only one sentence per commit and use the description.
- **Retroactive changes**: If you change something in a later commit that was introduced in an earlier commit, reference it.

### Code Style

New contributions should be created according to the following guidelines:

- **[Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)**: Rules for committing to the Django framework
- **[PEP 8](https://peps.python.org/pep-0008/)**: Style Guide for Python Code
- **[SOLID Principles](https://medium.com/@umaparvat/solid-principles-in-python-c9c3c337e0e1)**: The five golden rules of OOP
- **[DRY](https://docs.getdbt.com/terms/dry#why-write-dry-code)**: "Don't repeat yourself!"

## Join The Project Team

We are constantly looking for new core team members in the areas of software engineering, marketing & design.

### Requirements

_Italicized points_ are welcome but not required. In general, we require motivation, willingness to learn, a basic knowledge of software development, knowledge of German or English and a minimum age of 16 years.

#### Django Developer

As a Django developer, you'll be responsible for developing and maintaining the backend components of the web application, ensuring code quality and security. You'll implement new features and fix bugs according to project requirements, while closely collaborating with frontend developers to integrate user interfaces. Additionally, you'll participate in code reviews to help maintain overall code quality.

**Skills**:

- Good knowledge of Django (6 months of experience or equivalent through project work)
- Experience with Python and common web technologies (HTML, CSS, JavaScript)
- Familiarity with databases (PostgreSQL or SQLite) and ORM systems
- Knowledge of Git and Github
- _Knowledge of Docker and DDEV_
- _Knowledge of Alpine.js, Tailwind CSS and HTMX_
- _Ability to write unit tests with PyTest, Factory Boy and Faker for Django_

**Expectations**:

- Willingness to dive into the existing codebase.
- Proactive communication and regular progress updates.
- Ability to work in a collaborative, distributed team.

<!-- #### Machine Learning Engineer

As a machine learning engineer specializing in automated model training, you'll be responsible for developing and implementing robust processes for training ML models using diverse user-provided datasets. Your role involves designing automated pipelines, monitoring model performance, and ensuring accuracy and adaptability across various data inputs. You'll also collaborate with team members to integrate these automated systems into the broader project, while documenting processes and providing insights on model performance and potential improvements.

**Skills**:

- Basic to intermediate knowledge of machine learning algorithms and techniques.
- Familiarity with ML frameworks like TensorFlow, PyTorch, or Scikit-learn.
- Experience with data processing and analysis using tools like Pandas, NumPy, or similar.
- Knowledge of Git and Github
- _Knowledge of Docker and DDEV_
- _Knowledge of Django & Django REST_
- _Ability to write unit tests with PyTest_
- _Knowledge of cloud-based ML services (e.g., Google AI, AWS SageMaker) for scalable model training._
- _Experience with deploying models and managing model versioning and updates._

**Expectations**:

- Develop systems to automate the training of models based on user-provided datasets, including handling data validation and preprocessing.
- Regular communication and updates on model performance and improvements.
- Collaborate with the development team to integrate automated ML solutions into the existing infrastructure. -->

#### Web Designer (UI/UX)

As a web designer, you'll be tasked with creating visually appealing and user-friendly interfaces across various devices and platforms. Your responsibilities include developing and maintaining design guidelines, crafting layouts, icons, and other visual elements to ensure a consistent user experience. Collaborating closely with developers will be crucial to ensure the correct implementation of your designs.

**Skills**:

- Strong knowledge of web design and user experience design.
- Experience with design tools like Adobe XD, Penpot, Figma, Sketch, or similar.
- _Knowledge of HTML and CSS to support frontend development._
- _Experience with creating SVG and 2D graphics_

**Expectations**:

- Ability to analyze user feedback and integrate improvements.
- Regular communication and presentation of design ideas and progress.
- Flexibility to adjust designs based on technological or project requirements.

#### Social Media Manager

As a social media and content manager, you'll be responsible for increasing project visibility and engagement through creative strategies across multiple platforms. Your role involves creating and managing content for TikTok, Instagram, and a blog, including video production, post scheduling, and community engagement. You'll also need to stay on top of social media trends, analyze performance metrics, and continuously refine marketing efforts to maximize reach and impact.

**Skills**:

- Experience in social media marketing with a focus on TikTok and Instagram.
- Experience in writing and managing blog content.
- _Knowledge of Google Ads_
- _Knowledge of SEO Optimization_
- _Knowledge of graphic design tools (e.g., Canva, Adobe Spark, DaVinci) for creating visual content._

**Expectations**:

- Creativity in developing new and engaging content ideas tailored to TikTok and Instagram audiences.
- Regularly update and manage blog content, including SEO optimization and audience engagement.
- Analyze social media metrics and blog performance to optimize content strategies.

### Benefits

Unfortunately, we cannot offer you any payment at the moment. However, after the product is released, the plan is to split the excess revenue (i.e. the part of the sales that is not already planned) among the core team.
<br>
However, we do offer you other cool benefits:

- You work on a cool project with a cool team
- A letter of recommendation upon request
- Participation in internal team voting and thus direct influence on the development of the project

### Join Us

If you are interested in joining us, please send your application to gall.dev@proton.me. Thank you for your interest in participating in this project!

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://contributor-covenant.org/), version
[1.4](https://www.contributor-covenant.org/version/1/4/code-of-conduct/code_of_conduct.md) and
[2.0](https://www.contributor-covenant.org/version/2/0/code_of_conduct/code_of_conduct.md),
and was generated by [contributing-gen](https://github.com/bttger/contributing-gen).
