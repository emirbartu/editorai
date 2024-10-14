import moduller.velhasil as velhasil
from moduller.atasozlerOneri import AtasozleriOneri

def test_velhasil():
    print("Testing Velhasil class...")
    test_text = "Bu bir test cümlesidir. Bu ikinci cümledir."
    v = velhasil.Velhasil(test_text)
    result = v.yazimDenetimi(test_text)
    print(f"Yazım denetimi sonucu: {result}")

    print("\nTesting cumleBulucu...")
    paragraflar = v.paragrafAyir(test_text)
    cumleler = v.cumleBulucu(paragraflar)
    print(f"Bulunan cümleler: {cumleler}")

    print("\nTesting cumleBolucu...")
    bolunebilir = v.cumleBolucu(test_text)
    print(f"Cümle bölünebilir mi?: {bolunebilir}")

def test_atasozlerOneri():
    print("\nTesting AtasozleriOneri...")
    atasozleri = AtasozleriOneri()
    oneri = atasozleri.atasozuBul("test cümlesi")
    print(f"Atasözü önerisi: {oneri}")

if __name__ == "__main__":
    test_velhasil()
    test_atasozlerOneri()

print("\nAll tests completed.")
