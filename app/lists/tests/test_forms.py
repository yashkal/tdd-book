from lists.forms import EMPTY_ITEM_ERROR, ItemForm


def test_form_renders_item_text_input():
    form = ItemForm()
    assert 'placeholder="Enter a to-do item"' in form.as_p()
    assert 'class="form-control input-lg"' in form.as_p()


def test_form_validation_for_blank_items():
    form = ItemForm(data={"text": ""})
    assert form.is_valid() is False
    assert form.errors["text"] == [EMPTY_ITEM_ERROR]
