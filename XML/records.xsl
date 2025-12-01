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
      </head>

      <body>
        <!-- Top Navigation -->
        <nav class="topnav">
          <!-- Logo -->
          <div class="logo">
            <a href="../home.html">
              <img src="../images/logo.png" alt="Logo" class="logo-image"/>
            </a>
          </div>

          <!-- Navigation Links -->
          <ul class="nav-links">
            <li><a href="../home.html">Home</a></li>
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
                <img src="../images/collection.gif" alt="Record wall" class="hero-record-image"/>
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

                      <button class="product-button product-button-secondary">
                        View Product
                      </button>
                    </div>
                  </div>
                </xsl:for-each>
              </div>
            </div>
          </section>

        </main>
      </body>
    </html>

  </xsl:template>
</xsl:stylesheet>
