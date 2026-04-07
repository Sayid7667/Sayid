import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import time
import re
from datetime import datetime

def scrape_wikipedia_countries():
    """Scraping data negara dari Wikipedia Indonesia"""
    
    url = "https://id.wikipedia.org/wiki/Daftar_negara_di_dunia"
    
    # Header agar tidak diblokir
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
    }
    
    print(f"📡 Mengakses {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Gagal mengambil data. Status code: {response.status_code}")
        return []
    
    print("✅ Berhasil mengakses Wikipedia\n")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    countries_data = []
    
    # Cari semua tabel dengan class wikitable
    tables = soup.find_all('table', class_='wikitable')
    
    if not tables:
        print("❌ Tidak menemukan tabel data")
        return []
    
    print(f"📌 Menemukan {len(tables)} tabel")
    
    # Ambil tabel pertama (biasanya daftar negara)
    table = tables[0]
    rows = table.find_all('tr')
    
    print(f"📌 Memproses data...\n")
    
    # Lewati baris header
    for idx, row in enumerate(rows[1:], 1):
        try:
            cols = row.find_all('td')
            
            if len(cols) >= 2:
                # Nama negara
                country_name = cols[0].get_text(strip=True)
                # Bersihkan dari karakter aneh
                country_name = re.sub(r'\[.*?\]', '', country_name)
                
                # Ibu kota
                capital = cols[1].get_text(strip=True) if len(cols) > 1 else "-"
                capital = re.sub(r'\[.*?\]', '', capital)
                
                # Luas wilayah (km²)
                area = cols[2].get_text(strip=True) if len(cols) > 2 else "-"
                area = re.sub(r'\[.*?\]', '', area)
                
                # Populasi (jika ada)
                population = cols[3].get_text(strip=True) if len(cols) > 3 else "-"
                population = re.sub(r'\[.*?\]', '', population)
                
                # Kepadatan penduduk (jika ada)
                density = cols[4].get_text(strip=True) if len(cols) > 4 else "-"
                density = re.sub(r'\[.*?\]', '', density)
                
                # Benua
                continent = cols[5].get_text(strip=True) if len(cols) > 5 else "-"
                continent = re.sub(r'\[.*?\]', '', continent)
                
                # Mata uang
                currency = "-"
                if len(cols) > 6:
                    currency = cols[6].get_text(strip=True)
                    currency = re.sub(r'\[.*?\]', '', currency)
                
                # Hanya simpan jika nama negara tidak kosong
                if country_name and len(country_name) > 1:
                    countries_data.append({
                        'no': idx,
                        'negara': country_name,
                        'ibu_kota': capital,
                        'luas_wilayah_km2': area,
                        'populasi': population,
                        'kepadatan_km2': density,
                        'benua': continent,
                        'mata_uang': currency,
                        'sumber': 'Wikipedia Indonesia',
                        'waktu_scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    print(f"✓ [{idx}] {country_name} - {capital} ({continent})")
                    time.sleep(0.05)  # Jeda kecil
                    
        except Exception as e:
            print(f"✗ Error pada baris {idx}: {e}")
            continue
    
    return countries_data

def scrape_indonesia_provinces():
    """Bonus: Scraping data provinsi di Indonesia"""
    
    url = "https://id.wikipedia.org/wiki/Daftar_provinsi_di_Indonesia"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    print("\n📡 Mengakses data provinsi Indonesia...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("❌ Gagal mengambil data provinsi")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    provinces_data = []
    
    # Cari tabel provinsi
    tables = soup.find_all('table', class_='wikitable')
    
    if tables:
        table = tables[0]
        rows = table.find_all('tr')[1:]  # Skip header
        
        for idx, row in enumerate(rows[:34], 1):  # 34 provinsi
            try:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    province_name = cols[1].get_text(strip=True) if len(cols) > 1 else "-"
                    province_name = re.sub(r'\[.*?\]', '', province_name)
                    
                    capital = cols[2].get_text(strip=True) if len(cols) > 2 else "-"
                    capital = re.sub(r'\[.*?\]', '', capital)
                    
                    area = cols[3].get_text(strip=True) if len(cols) > 3 else "-"
                    area = re.sub(r'\[.*?\]', '', area)
                    
                    provinces_data.append({
                        'no': idx,
                        'provinsi': province_name,
                        'ibu_kota': capital,
                        'luas_wilayah_km2': area,
                        'sumber': 'Wikipedia Indonesia'
                    })
                    
                    print(f"  ✓ {idx}. {province_name} - {capital}")
                    time.sleep(0.05)
            except:
                continue
    
    return provinces_data

def save_to_json(data, filename='hasil_wikipedia/countries.json'):
    """Menyimpan data ke file JSON"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Data disimpan ke {filename}")

def save_to_csv(data, filename='hasil_wikipedia/countries.csv'):
    """Menyimpan data ke file CSV"""
    if not data:
        print("Tidak ada data untuk disimpan")
        return
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    print(f"💾 Data disimpan ke {filename}")

def print_statistics(data):
    """Menampilkan statistik data negara"""
    if not data:
        return
    
    print("\n" + "="*60)
    print("📊 STATISTIK DATA NEGARA")
    print("="*60)
    
    # Hitung per benua
    continents = {}
    for item in data:
        benua = item['benua']
        if benua and benua != "-":
            continents[benua] = continents.get(benua, 0) + 1
    
    if continents:
        print("\n🌏 Berdasarkan Benua:")
        for benua, count in sorted(continents.items(), key=lambda x: x[1], reverse=True):
            print(f"   {benua}: {count} negara")
    
    # 5 negara terluas
    print("\n🏔️ 5 Negara Terluas:")
    area_list = []
    for item in data:
        area_str = item['luas_wilayah_km2']
        # Extract angka dari string
        numbers = re.findall(r'[\d,\.]+', area_str)
        if numbers:
            try:
                area_num = float(numbers[0].replace(',', '').replace('.', ''))
                area_list.append((item['negara'], area_num, area_str))
            except:
                pass
    
    area_list.sort(key=lambda x: x[1], reverse=True)
    for i, (negara, _, area_str) in enumerate(area_list[:5], 1):
        print(f"   {i}. {negara}: {area_str}")
    
    print(f"\n📈 Total negara: {len(data)}")
    print(f"🕐 Waktu scraping: {data[0]['waktu_scraping']}")

def print_country_details(data, country_name=None):
    """Mencari dan menampilkan detail negara tertentu"""
    if not country_name:
        return
    
    print("\n" + "="*60)
    print(f"🔍 MENCARI NEGARA: {country_name.upper()}")
    print("="*60)
    
    found = False
    for item in data:
        if country_name.lower() in item['negara'].lower():
            print(f"\n✅ Ditemukan!")
            print(f"   📍 Nama: {item['negara']}")
            print(f"   🏙️  Ibu Kota: {item['ibu_kota']}")
            print(f"   🌍 Benua: {item['benua']}")
            print(f"   📏 Luas: {item['luas_wilayah_km2']}")
            print(f"   👥 Populasi: {item['populasi']}")
            print(f"   💰 Mata Uang: {item['mata_uang']}")
            found = True
            break
    
    if not found:
        print(f"\n❌ Negara '{country_name}' tidak ditemukan")

def main():
    print("\n" + "="*60)
    print("🌏 WEB SCRAPING WIKIPEDIA - DATA NEGARA DUNIA")
    print("="*60 + "\n")
    
    # Scraping data negara
    countries = scrape_wikipedia_countries()
    
    if countries:
        print(f"\n✅ Berhasil mengambil {len(countries)} negara")
        
        # Simpan ke file
        save_to_json(countries, 'hasil_wikipedia/countries.json')
        save_to_csv(countries, 'hasil_wikipedia/countries.csv')
        
        # Tampilkan statistik
        print_statistics(countries)
        
        # Cari negara tertentu (contoh: Indonesia)
        print_country_details(countries, "Indonesia")
        
        # Tanya apakah mau scraping data provinsi juga
        print("\n" + "="*60)
        jawab = input("📌 Apakah ingin scraping data provinsi Indonesia juga? (y/n): ")
        
        if jawab.lower() == 'y':
            print("\n" + "="*60)
            print("🏝️ SCRAPING DATA PROVINSI INDONESIA")
            print("="*60 + "\n")
            
            provinces = scrape_indonesia_provinces()
            
            if provinces:
                save_to_json(provinces, 'hasil_wikipedia/indonesia_provinces.json')
                save_to_csv(provinces, 'hasil_wikipedia/indonesia_provinces.csv')
                print(f"\n✅ Berhasil mengambil {len(provinces)} provinsi")
        
        # Preview 10 negara pertama
        print("\n" + "="*60)
        print("📋 PREVIEW 10 NEGARA PERTAMA")
        print("="*60)
        for item in countries[:10]:
            print(f"\n{item['no']}. {item['negara']}")
            print(f"   🏙️  {item['ibu_kota']} | 🌍 {item['benua']}")
        
        print("\n" + "="*60)
        print("✨ SCRAPING SELESAI!")
        print(f"📁 File tersimpan di folder: hasil_wikipedia/")
        print("="*60)
        
    else:
        print("\n❌ Gagal mengambil data. Mungkin struktur Wikipedia berubah.")
        print("💡 Tips: Coba jalankan lagi nanti atau periksa koneksi internet")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proses dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Terjadi error: {e}")
        print("💡 Pastikan koneksi internet stabil")