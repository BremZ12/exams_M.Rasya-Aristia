import streamlit as st
import pandas as pd
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Web Crawler Search - Books",
    page_icon="📚",
    layout="wide"
)

# Custom CSS untuk tampilan lebih menarik
st.markdown("""
<style>
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling untuk hasil */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
        transition: transform 0.2s;
    }
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .book-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    .book-price {
        background: #27ae60;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: 600;
    }
    .book-availability {
        padding: 0.2rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .in-stock {
        background: #d4edda;
        color: #155724;
    }
    .out-of-stock {
        background: #f8d7da;
        color: #721c24;
    }
    
    /* Search box styling */
    .search-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    /* Metric styling */
    .metric-container {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    .metric-label {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        padding: 0.5rem 0;
    }
    .sidebar-section h4 {
        color: #2c3e50;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 0.8rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #7f8c8d;
        border-top: 1px solid #ecf0f1;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header utama dengan gradient
st.markdown("""
<div class="main-header">
    <h1>📚 Web Crawler Search</h1>
    <p>Data buku dari <strong>Books to Scrape</strong> menggunakan Scrapy</p>
</div>
""", unsafe_allow_html=True)

# Load data
DATA_PATH = "books.csv"

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    
    # Sidebar - Filter dan Informasi
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/book.png", width=80)
        st.markdown("## 🎯 Filter Pencarian")
        
        # Statistik ringkas
        st.markdown("### 📊 Statistik")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📚 Total Buku", len(df))
        with col2:
            tersedia = df["Availability"].str.contains("In stock", case=False).sum()
            st.metric("✅ Tersedia", tersedia)
        
        st.markdown("---")
        
        # Filter tambahan
        st.markdown("### 🔍 Filter Lanjutan")
        
        
        # Rentang harga
        if 'Price' in df.columns:
            df['Price'] = df['Price'].astype(str).str.replace('£', '').str.replace(',', '').astype(float)
            min_price = float(df['Price'].min())
            max_price = float(df['Price'].max())
            price_range = st.slider(
                "Rentang Harga (£)",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price),
                step=0.5
            )
        
        # Pilihan tampilan
        st.markdown("### ⚙️ Tampilan")
        view_mode = st.radio(
            "Mode Tampilan",
            ["Card View", "Table View"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #7f8c8d; font-size: 0.8rem;">
            <p>📅 UAS Information Retrieval</p>
            <p>SIF502 - Genap 2025/2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content - Pencarian
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    col_search1, col_search2 = st.columns([3, 1])
    with col_search1:
        query = st.text_input(
            "🔍 Cari judul buku atau nama penulis:",
            placeholder="Ketik kata kunci di sini...",
            label_visibility="collapsed"
        )
    with col_search2:
        search_type = st.selectbox(
            "Cari berdasarkan",
            ["Judul"],
            label_visibility="collapsed"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter data berdasarkan pencarian
    filtered_df = df.copy()
    
    
    # Terapkan filter harga
    if 'Price' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['Price'] >= price_range[0]) & 
            (filtered_df['Price'] <= price_range[1])
        ]
    
    # Terapkan filter pencarian
    if query:
        filtered_df = filtered_df[
            filtered_df["Title"].str.contains(query, case=False, na=False)
        ]
    
    # Tampilkan hasil
    if len(filtered_df) > 0:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h3>📖 Hasil Pencarian</h3>
            <span style="background: #667eea; color: white; padding: 0.3rem 1.2rem; border-radius: 20px; font-weight: 600;">
                {len(filtered_df)} buku ditemukan
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if view_mode == "Card View":
            # Card View
            for _, row in filtered_df.iterrows():
                price_display = f"£{row['Price']:.2f}" if 'Price' in row else "N/A"
                availability_class = "in-stock" if 'In stock' in str(row.get('Availability', '')) else "out-of-stock"
                availability_text = row.get('Availability', 'Tersedia') if pd.notna(row.get('Availability')) else "Tersedia"

                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <div class="book-title">📕 {row['Title']}</div>
                            <div style="margin-top: 0.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                <span class="book-price">{price_display}</span>
                                <span class="book-availability {availability_class}">{availability_text}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            # Table View
            st.dataframe(
                filtered_df,
                use_container_width=True
            )
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 12px;">
            <h3 style="color: #7f8c8d;">🔍 Tidak ada buku yang ditemukan</h3>
            <p style="color: #95a5a6;">Coba kata kunci lain atau reset filter</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("⚠️ Data belum tersedia. Jalankan crawler terlebih dahulu.")
    st.info("""
    **Cara menjalankan crawler:**
    1. Buka terminal di folder `scrapy_project`
    2. Jalankan: `scrapy crawl books -o ../books.csv`
    3. Pastikan file `books.csv` berada di direktori yang sama dengan `app.py`
    """)

# Footer
st.markdown("""
<div class="footer">
    <p>📚 Web Crawler Search App | UAS Information Retrieval (SIF502) | Genap 2025/2026</p>
    <p style="font-size: 0.8rem;">Dosen Pengampu: Teuku Rizky Noviandy, S.Kom., M.Kom.</p>
</div>
""", unsafe_allow_html=True)
