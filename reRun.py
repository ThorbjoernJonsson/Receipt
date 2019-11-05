from Receipt import download
from Receipt import scan_receipt
from Receipt import save_receipts

download.run_thr_em()
scanner = scan_receipt.ScanReceipts()
scanner.create_photos()
save_receipts.save_receipts()