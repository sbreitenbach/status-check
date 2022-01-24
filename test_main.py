import main

# These two tests can be removed 
# They simply serve as inital environment setup checks
def test_plways_passes():
    a = 1
    assert(a==1) 

GSD1 = "test_resources/gsd1.jpeg"
GSD2 = "test_resources/gsd2.jpeg"
GSD3 = "test_resources/gsd3.jpeg"

def test_image_compare_same():
    assert(main.compare_images(GSD1, GSD1) == 1.0)

def test_image_compare_diff_1():
    assert(main.compare_images(GSD1, GSD2) < 0.75)

def test_image_compare_diff_2():
    assert(main.compare_images(GSD1, GSD3) < 0.9)
