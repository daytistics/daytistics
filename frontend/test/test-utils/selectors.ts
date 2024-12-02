import type { VueWrapper } from '@vue/test-utils';

function findByText(wrapper: VueWrapper, selector: string, text: RegExp) {
    return wrapper.findAll(selector).filter((element) => element.text().match(text));
}

function findByAttribute(wrapper: VueWrapper, selector: string, attribute: string, value: string) {
    return wrapper.findAll(selector).filter((element) => element.attributes(attribute) === value);
}

export { findByText, findByAttribute };
