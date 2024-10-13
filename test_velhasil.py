from velhasil import Velhasil

def test_velhasil():
    test_text = "Bu bir test cümlesidir. Velhasil projesini test ediyoruz."
    v = Velhasil(test_text)

    print(f"Test metni: {test_text}")
    print(f"Kelime sayısı: {v.kelimesayisi}")
    print(f"Karakter sayısı: {v.karaktersayisi}")
    print(f"Cümle sayısı: {v.cumleSayisi}")
    print(f"Benzersiz kelime sayısı: {v.benzersizkelimesayisi}")
    print(f"Paragraf sayısı: {v.paragrafSayisi}")

    spell_check_result = v.yazimDenetimi(test_text)
    print(f"Yazım denetimi sonucu: {spell_check_result}")

if __name__ == "__main__":
    test_velhasil()