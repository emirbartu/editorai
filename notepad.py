import gradio as gr
import moduller.atasozlerOneri as atasozlerOneri
import moduller.velhasil as velhasil
import pytesseract
from PIL import Image

class VelhasilApp:
    def __init__(self):
        self.velhasil_ = velhasil.Velhasil()
    
    def file_open(self, file):
        try:
            with open(file.name, 'r', encoding="UTF-8") as f:
                text = f.read()
            return text, f"Opened file: {file.name}"
        except Exception as e:
            return "", f"Error: {str(e)}"

    def atasozuOneri(self, text):
        atasozleri_ = atasozlerOneri.AtasozleriOneri()
        oneriler = atasozleri_.atasozuBul(text)
        oneriler.sort(reverse=True)
        return "Atasözü Önerisi Bulunamadı..." if len(oneriler) == 0 else "\n".join(oneriler)

    def yazimDenetimi(self, text):
        # Denetim sonuçları: kelimeler ve karşılık gelen hata kodları
        kelimeler = text.split()  # Metni kelimelere ayırıyoruz
        denetim_kodlari = self.velhasil_.yazimDenetimi(text.rstrip())  # Hata kodları listesi

        # Hata kodlarına ait açıklamalar
        error_codes = {
            0: "Kelime doğru",
            1: "Kelime bir noktalama işareti, önündeki boşluk silinmeli",
            2: "Kelime yanlış",
            3: "Cümleden sonra nokta koyulmalı",
            4: "Noktalama işaretinden sonra boşluk bırakılmalı",
            5: "Noktadan sonra büyük harf gelmeli",
            6: "Kelime doğru ancak Türkçe kelime önerisi var"
        }

        # Renklendirme için hata kodlarına ait renkler
        color_map = {
            0: "green",
            1: "orange",
            2: "red",
            3: "blue",
            4: "purple",
            5: "yellow",
            6: "cyan"
        }

        # Kelimeler ve hata kodlarını eşleştirip her kelimenin karşısına açıklama ekliyoruz
        formatted_output = [
            (kelime, color_map.get(kod, None)) for kelime, kod in zip(kelimeler, denetim_kodlari)
        ]

        return formatted_output

    def istatistikGoster(self, text):
        velhasil__ = velhasil.Velhasil(text)
        stats = [
            f"Kelime sayısı: {velhasil__.kelimesayisi}",
            f"Benzersiz kelime sayısı: {velhasil__.benzersizkelimesayisi}",
            f"Karakter sayısı: {velhasil__.karaktersayisi}",
            f"Benzersiz karakter sayısı: {velhasil__.benzersizkaraktersayisi}",
            f"Paragraf sayısı: {velhasil__.paragrafSayisi}",
            f"Cümle sayısı: {velhasil__.cumleSayisi}",
            f"Kelimeler: {velhasil__.benzersizkelimeler}"
        ]
        return "\n".join(stats)

    def cumleAnalizi(self, text):
        velhasil__ = velhasil.Velhasil(text)
        bolunebilen_cumle_sayisi = 0
        highlighted_sentences = []

        for cumle in velhasil__.cumleler:
            cumle_bolme_sonucu = velhasil__.cumleBolucu(cumle)
            if cumle_bolme_sonucu != 0:  # 0 olmayan sonuçları vurguluyoruz
                highlighted_sentences.append((cumle, "highlight"))  # highlight olan cümleler
                bolunebilen_cumle_sayisi += 1
            else:
                highlighted_sentences.append((cumle, None))  # vurgulanmayan cümleler

        analysis = [
            f"Metnin içinde {velhasil__.cumleSayisi} cümle bulundu.",
            f"Metnin içinde {bolunebilen_cumle_sayisi} bölünmeye müsait cümle bulundu.",
            "Metnin daha okunabilir olması için işaretlenen birleşik cümleleri bölebilirsiniz.",
            f"Metin {velhasil__.paragrafSayisi} paragraftan oluşuyor."
        ]
        return highlighted_sentences, "\n".join(analysis)


    def process_captured_image(self, image):
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        try:
            text = pytesseract.image_to_string(image, lang='tur')
            return text
        except Exception as e:
            return f"OCR işlemi sırasında hata oluştu: {str(e)}"

    def run_app(self):
        with gr.Blocks(title="EditorAI - Metin İşleme Aracı") as demo:
            gr.Markdown("EditorAI Metin İşleme Aracı")

            with gr.Row():
                text_box = gr.Textbox(placeholder="Metninizi buraya yazın...", lines=10, label="Metin")

            with gr.Row():
                open_button = gr.File(label="Dosya Aç", scale=1)
            with gr.Row():
                image_input = gr.Image(label="Resim Yükle", mirror_webcam=False, scale=1)
            with gr.Column():
                with gr.Row():
                    atasozu_button = gr.Button("Atasözü Öner")
                    yazimdenetim_button = gr.Button("Yazım Denetimi")
                with gr.Row():
                    istatistik_button = gr.Button("Metin İstatistikleri")
                    cumleanalizi_button = gr.Button("Cümle Analizi")

                highlighted_output = gr.HighlightedText(
                    label="Yazım Denetimi Sonuçları", 
                    combine_adjacent=True, 
                    color_map={"green": "green", "orange": "orange", "red": "red", "blue": "blue", "purple": "purple", "yellow": "yellow", "cyan": "cyan"},
                    scale=4
                )

            output_text = gr.Textbox(label="Çıktı", interactive=False)
            open_button.upload(self.file_open, inputs=[open_button], outputs=[text_box, output_text])
            atasozu_button.click(self.atasozuOneri, inputs=[text_box], outputs=[output_text])
            yazimdenetim_button.click(self.yazimDenetimi, inputs=[text_box], outputs=[highlighted_output])
            istatistik_button.click(self.istatistikGoster, inputs=[text_box], outputs=[output_text])
            cumleanalizi_button.click(self.cumleAnalizi, inputs=[text_box], outputs=[highlighted_output, output_text])
            image_input.upload(self.process_captured_image, inputs=[image_input], outputs=[text_box])

        demo.launch()


if __name__ == "__main__":
    
    app = VelhasilApp()
    app.run_app()
