<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <!-- Main template -->
  <xsl:template match="/">

    <html>
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1"/>
        <title>Record Collection</title>
        <link rel="stylesheet" type="text/css" href="../styles.css"/>
        <link rel="icon" type="image/x-icon" href="../images/store_logo.png"/>
      </head>

      <body>
        <!-- Top Navigation -->
        <nav class="topnav">
          <!-- Logo -->
          <div class="logo">
            <a href="../index.html">
              <img src="../images/store_logo.png" alt="Logo" class="logo-image"/>
            </a>
          </div>

          <!-- Navigation Links -->
          <ul class="nav-links">
            <li><a href="../index.html">Home</a></li>
            <li><a href="records.xml" class="active-link">Collections</a></li>
            <li><a href="../about.html">About Us</a></li>
          </ul>

          <!-- Search Bar -->
          <div class="searchbar">
            <img src="../images/search-icon(white).png" alt="Search Icon" class="search-icon"/>
            <input type="text" placeholder="Search products..." class="search-input"/>
          </div>
        </nav>

        <!-- MAIN CONTENT -->
        <main class="page">

          <!-- Hero section -->
          <section class="hero">
            <div class="hero-inner">
              <div class="hero-text">
                <p class="hero-tagline">Seraphim Records</p>
                <h1>OUR COLLECTIONS</h1>
                <p class="hero-description">
                  Browse through our curated catalogue of albums.
                  Discover classics, hidden gems, and new favourites.
                </p>
                <div class="hero-buttons">
                  <a href="../home.html" class="btn btn-outline">Back Home</a>
                  <a href="#in-stock" class="btn btn-primary">View Records</a>
                </div>
              </div>

              <div class="hero-image-wrapper">
                <img src="../images/collection_player.gif"
                     alt="Record wall"
                     class="hero-record-image"/>
              </div>
            </div>
          </section>

          <!-- Collections grid on beige background -->
          <section class="collections-page" id="in-stock">
            <h2 class="collections-title">In Stock</h2>

            <div class="product-section">
              <div class="product-grid">
                <!-- Loop through all albums from this XML file -->
                <xsl:for-each select="records/album">
                  <div class="product-card">
                    <div class="product-image">
                      <img>
                        <xsl:attribute name="src">
                          <xsl:value-of select="cover_medium"/>
                        </xsl:attribute>
                        <xsl:attribute name="alt">
                          <xsl:value-of select="title"/>
                        </xsl:attribute>
                      </img>
                    </div>

                    <div class="product-info">
                      <h3 class="product-title">
                        <xsl:value-of select="title"/>
                      </h3>
                      <p class="product-artist">
                        <xsl:value-of select="artist"/>
                      </p>
                      <p class="product-price">
                        £<xsl:value-of select="price"/>
                      </p>

                      <!-- View Product button with Spotify data attributes -->
                      <button class="product-button product-button-secondary">
                        <xsl:attribute name="data-title">
                          <xsl:value-of select="title"/>
                        </xsl:attribute>
                        <xsl:attribute name="data-artist">
                          <xsl:value-of select="artist"/>
                        </xsl:attribute>
                        <xsl:attribute name="data-spotify">
                          <xsl:value-of select="spotify_embed"/>
                        </xsl:attribute>
                        View Product
                      </button>
                    </div>
                  </div>
                </xsl:for-each>
              </div>
            </div>
          </section>

        </main>

        <!-- Product modal for Spotify embed -->
        <div id="product-modal" class="product-modal">
          <div class="product-modal-content">
            <button class="product-modal-close" type="button">&#215;</button>

            <h3 id="product-modal-title"></h3>
            <p id="product-modal-artist" class="product-modal-artist"></p>

            <div class="product-modal-player">
              <iframe
                id="product-modal-spotify"
                style="border-radius:12px"
                src=""
                width="100%"
                height="352"
                frameborder="0"
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                loading="lazy">
              </iframe>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <footer class="footer">
          <div class="footer-top">
            <div class="social-icons">
              <img src="../images/facebook.png" alt="Facebook Icon" class="social-icon"/>
              <img src="../images/instagram.png" alt="Instagram Icon" class="social-icon"/>
            </div>
          </div>
          <div class="footer-bottom">
            <p>© 2024 Seraphim Records. All rights reserved.</p>
          </div>
        </footer>

        <!-- Modal script -->
        <script>
          document.addEventListener("DOMContentLoaded", function () {
            var grid = document.querySelector(".product-grid");
            var modal = document.getElementById("product-modal");
            var titleEl = document.getElementById("product-modal-title");
            var artistEl = document.getElementById("product-modal-artist");
            var iframe = document.getElementById("product-modal-spotify");
            var closeBtn = document.querySelector(".product-modal-close");

            if (!grid || !modal) return;

            grid.addEventListener("click", function (e) {
              var btn = e.target.closest(".product-button");
              if (!btn) return;

              var spotify = btn.getAttribute("data-spotify");
              if (!spotify) return;

              titleEl.textContent = btn.getAttribute("data-title") || "";
              artistEl.textContent = btn.getAttribute("data-artist") || "";
              iframe.src = spotify;

              modal.classList.add("open");
            });

            function closeModal() {
              modal.classList.remove("open");
              iframe.src = "";
            }

            closeBtn.addEventListener("click", closeModal);

            modal.addEventListener("click", function (e) {
              if (e.target === modal) {
                closeModal();
              }
            });

            document.addEventListener("keydown", function (e) {
              if (e.key === "Escape") {
                closeModal();
              }
            });
          });
        </script>

      </body>
    </html>

  </xsl:template>
</xsl:stylesheet>
