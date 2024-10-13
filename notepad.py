import gradio as gr
import atasozlerOneri
import velhasil
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
        corrected_text = self.velhasil_.yazimDenetimi(text.rstrip())
        return corrected_text

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
        highlighted_text = ""
        bolunebilen_cumle_sayisi = 0

        for cumle in velhasil__.cumleler:
            if velhasil__.cumleBolucu(cumle) == 1:
                highlighted_text += f'<span style="background-color: yellow">{cumle}</span> '
                bolunebilen_cumle_sayisi += 1
            else:
                highlighted_text += cumle + " "

        analysis = [
            f"Metnin içinde {velhasil__.cumleSayisi} cümle bulundu.",
            f"Metnin içinde {bolunebilen_cumle_sayisi} bölünmeye müsait cümle bulundu.",
            "Metnin daha okunabilir olması için işaretlenen birleşik cümleleri bölebilirsiniz.",
            f"Metin {velhasil__.paragrafSayisi} paragraftan oluşuyor."
        ]
        return highlighted_text, "\n".join(analysis)

    def process_captured_image(self, image):
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        try:
            text = pytesseract.image_to_string(image, lang='tur')
            return text
        except Exception as e:
            return f"OCR işlemi sırasında hata oluştu: {str(e)}"

    def run_app(self):
        with gr.Blocks() as demo:
            gr.Markdown("## Velhasıl... Metin İşleme Aracı")

            with gr.Row():
                text_box = gr.Textbox(placeholder="Metninizi buraya yazın...", lines=10, label="Metin")

            with gr.Row():
                open_button = gr.File(label="Dosya Aç")
                atasozu_button = gr.Button("Atasözü Öner")
                yazimdenetim_button = gr.Button("Yazım Denetimi")
                istatistik_button = gr.Button("Metin İstatistikleri")
                cumleanalizi_button = gr.Button("Cümle Analizi")
                image_input = gr.Image(label="Resim Yükle", mirror_webcam=False)

            output_text = gr.Textbox(label="Çıktı", interactive=False)

            open_button.upload(self.file_open, inputs=[open_button], outputs=[text_box, output_text])
            atasozu_button.click(self.atasozuOneri, inputs=[text_box], outputs=[output_text])
            yazimdenetim_button.click(self.yazimDenetimi, inputs=[text_box], outputs=[output_text])
            istatistik_button.click(self.istatistikGoster, inputs=[text_box], outputs=[output_text])
            cumleanalizi_button.click(self.cumleAnalizi, inputs=[text_box], outputs=[output_text, output_text])
            image_input.upload(self.process_captured_image, inputs=[image_input], outputs=[text_box])

        demo.launch()

if __name__ == "__main__":
    
    app = VelhasilApp()
    app.run_app()
