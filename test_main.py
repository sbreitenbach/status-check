import main

# These two tests can be removed 
# They simply serve as inital environment setup checks
def test_plways_passes():
    a = 1
    assert(a==1) 

GSD1 = "test_resources/gsd1.jpeg"
GSD2 = "test_resources/gsd2.jpeg"
GSD3 = "test_resources/gsd3.jpeg"
TEXT_IMAGE = "test_resources/text.jpeg"

def test_image_compare_same():
    assert(main.compare_images(GSD1, GSD1) == 1.0)

def test_image_compare_diff_1():
    assert(main.compare_images(GSD1, GSD2) < 0.75)

def test_image_compare_diff_2():
    assert(main.compare_images(GSD1, GSD3) < 0.9)

def test_ocr_text():
    assert(main.extract_text_from_image(TEXT_IMAGE) == "test image")

def test_error_words_failing_full_word():
    assert(main.check_images_for_error_words("test_resources/", ["test"]) == False)

def test_error_words_failing_partial_word():
    assert(main.check_images_for_error_words("test_resources/", ["tes"]) == False)

def test_error_words_passing():
    assert(main.check_images_for_error_words("test_resources/", ["foo"]) == True)