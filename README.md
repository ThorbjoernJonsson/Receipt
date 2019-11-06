# Receipt
Downloads receipts from Gmail, filters them in a readable format, reads the name of the company, the price and the date of the receipt and with a popup asks if you want to save it in the folder suggested.

Description.
1) In your Gmail you need to create a label named Receipts. Furthermore, you need to create a rule that all emails with subject line Receipt and an attachment goes automatically to that label.
2) You need to allow less secured apps access Gmail. See https://devanswers.co/allow-less-secure-apps-access-gmail-account/
3) In the download file you need to change EMAIL_ACCOUNT and PASSWORD to matching what you have for Gmail.
4) You need the following packages installed:
4.a) pip install email
4.b) pip install scipy
4.c) pip install numpy
4.d) pip install scikit-learn
4.e) pip install opencv-python
4.f) pip install Pillow
4.g) pip install datetime
4.h) On https://digi.bib.uni-mannheim.de/tesseract/ dowload tesseract-ocr-w64-setup-v5.0.0-alpha.20191030. Save it under C:\Program Files\Tesseract-OCR\
 
Daily use.
Take a picture of the receipt, try to have the receipt cover big part of the photo and a dark plain background is best. Send the photo to your email address with the subject line Receipt. Import the package Receipt and the download will automatically start. To re download new receipts run the reRun module.

  
