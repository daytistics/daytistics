from django_components import Component, register, types

@register("spinner")
class Spinner(Component):
    def get_context_data(self, size: str = "w-32") -> dict:
        # Ensure that the `size` parameter is applied as both width and height
        return {
            'size': size,
            'height': size  # Apply the same size to height
        }

    template: types.django_html = """
        <div
            class="{{ size }} {{ height }} aspect-square rounded-full relative flex justify-center items-center animate-[spin_3s_linear_infinite] z-40 bg-[conic-gradient(white_0deg,white_300deg,transparent_270deg,transparent_360deg)] before:animate-[spin_2s_linear_infinite] before:absolute before:w-[60%] before:aspect-square before:rounded-full before:z-[80] before:bg-[conic-gradient(white_0deg,white_270deg,transparent_180deg,transparent_360deg)] after:absolute after:w-3/4 after:aspect-square after:rounded-full after:z-[60] after:animate-[spin_3s_linear_infinite] after:bg-[conic-gradient(#065f46_0deg,#065f46_180deg,transparent_180deg,transparent_360deg)]"
            >
            <span
                class="absolute w-[85%] aspect-square rounded-full z-[60] animate-[spin_5s_linear_infinite] bg-[conic-gradient(#34d399_0deg,#34d399_180deg,transparent_180deg,transparent_360deg)]"
            >
            </span>
        </div>
    """

    css = """"""
    js = """"""
