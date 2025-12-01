<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">

    <html>
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1"/>
        <title>Top Albums Collection</title>
        <link rel="stylesheet" type="text/css" href="../styles.css"/>
      </head>

      <body>
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
            <li><a href="records.xml">Collections</a></li>
            <li><a href="../aboutus.html">About Us</a></li>
          </ul>

          <!-- Search Bar -->
          <div class="searchbar">
            <img src="../images/search-icon(white).png" alt="Search Icon" class="search-icon"/>
            <input type="text" placeholder="Search products..." class="search-input"/>
          </div>
        </nav>

        <h1>Record Collection</h1>

        <!-- Slideshow container -->
        <div class="slideshow-container">
          <xsl:for-each select="document('top_records.xml')/top_albums/record">
            <div class="mySlides fade">
              <img>
                <xsl:attribute name="src">
                  <xsl:value-of select="cover_medium"/>
                </xsl:attribute>
                <xsl:attribute name="alt">
                  <xsl:value-of select="name"/>
                </xsl:attribute>
              </img>
              <div class="caption">
                <xsl:value-of select="name"/>
                <xsl:text> — </xsl:text>
                <xsl:value-of select="artist"/>
              </div>
            </div>
          </xsl:for-each>

          <!-- Next and previous buttons (ONLY navigation) -->
          <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
          <a class="next" onclick="plusSlides(1)">&#10095;</a>
        </div>

        <!-- No dots here -->

        <!-- Slideshow JS -->
        <script type="text/javascript">
        <![CDATA[
          let slideIndex = 1;

          function plusSlides(n) {
            showSlides(slideIndex += n);
          }

          function showSlides(n) {
            const slides = document.getElementsByClassName("mySlides");
            if (slides.length === 0) return;

            if (n > slides.length) { slideIndex = 1; }
            if (n < 1) { slideIndex = slides.length; }

            for (let i = 0; i < slides.length; i++) {
              slides[i].style.display = "none";
            }

            slides[slideIndex - 1].style.display = "block";
          }

          document.addEventListener("DOMContentLoaded", function() {
            showSlides(slideIndex);
          });
        ]]>
        </script>

      </body>
    </html>

  </xsl:template>

</xsl:stylesheet>
