
# **Numismatic Data Architecture: A Foundational Report on the Ten Priority Collector Markets**

This report provides the foundational data architecture for a comprehensive numismatic taxonomy, focusing on ten priority countries selected for their significant collector market size and numismatic complexity. The objective is to deliver structured, validated data suitable for ingestion into a relational database, while also providing the expert context necessary to inform schema design. The data covers issuing authorities (mints and printers), principal collectible coin and banknote types, unique dating systems, and notable numismatic "edge cases." This analysis will reveal how geopolitical events, economic pressures, and technological advancements have shaped the currency of these nations, offering critical insights for creating a robust and accurate numismatic catalog.

---

## **Part I: Numismatic Data Analysis by Priority Country**

---

### **Chapter 1: People's Republic of China (CNY)**

#### **1.1 Foundational Data**

* **Country Code:** CN 1  
* **Country Name:** People's Republic of China. The official name is *Zhōnghuá Rénmín Gònghéguó* (中华人民共和国).3  
* **Market Priority:** 1

#### **1.2 Issuing Authorities: Mints and Printers**

The production of currency in the People's Republic of China is managed by a single, vertically integrated state-owned enterprise, the China Banknote Printing and Minting Corporation (CBPMC). This entity operates under the direct authority of the People's Bank of China and is responsible for the entire lifecycle of the Renminbi, from design and research to the manufacturing of banknotes, coins, and their constituent materials.5

Banknote printing facilities are geographically dispersed across several major cities, including Beijing, Shanghai, Chengdu, Xi'an, Shijiazhuang, and Nanchang.7 Coinage is produced at dedicated mints in Nanjing, Shanghai, and Shenyang.6 The CBPMC's comprehensive structure also includes specialized subsidiaries for producing banknote paper in Baoding, Kunshan, and Chengdu; security inks through the China Banknote Ink Co Ltd; and security threads via the Zhongchao Special Security Technology Co Ltd.6

Modern Chinese coins do not feature mint marks to distinguish their facility of origin. This practice ensures national uniformity, making the specific minting location irrelevant for circulation purposes. Numismatists and researchers, however, can often differentiate between the products of various mints by analyzing minute variations in die characteristics, strike quality, and stylistic details.7 This contrasts sharply with historical coinage, particularly from the Qing Dynasty (1644-1911), which employed a complex system of Manchu and Chinese characters on the reverse of cash coins to explicitly identify the issuing mint.9 Similarly, modern banknotes do not carry explicit bureau codes to identify the printing plant of origin, though various printers existed historically, such as the Bureau of Engraving and Printing, Peking (BEPP).10

#### **1.3 Collectible Coin and Banknote Types**

The Chinese numismatic market is characterized by strong collector interest in modern precious metal issues, historical silver coinage from the Republic era, and specific series of banknotes from the People's Republic.

Key collectible coin types, identified through population reports and numismatic catalogs, span several historical periods.11 The modern Gold and Silver Panda series, issued from 1982 to the present, and the annual Lunar series, issued since 1981, are foundational to the modern collector market and have significant international demand. From the Republic Era (1912-1949), large silver dollars are exceptionally popular. Among the most sought-after are the Yuan Shikai "Fat Man" dollar, particularly from Year 3 (1914), and the Sun Yat-sen "Junk" dollar from Year 23 (1934). The high demand for these pieces has also made them some of the most frequently counterfeited Chinese coins.13 Imperial and provincial coinage from before 1911, such as Dragon Dollars and Cash coins from provinces like Chihli and Kwangtung, also command high collector interest.

Among banknotes, several series are highly prized by collectors.14 The third series of Renminbi, issued in the 1960s, is particularly popular, with the 1 Yuan note featuring China's first female tractor driver (Pick catalog number 874b) and the 2 Yuan note (P-875a2) being staples of the market.14 Modern commemorative issues also generate intense interest; the 2000 "Millennium Dragon" 100 Yuan note (P-902) and the 2015 "Aerospace" 100 Yuan note (P-910) are two of the most heavily collected and graded modern Chinese notes.14

#### **1.4 Dating Systems**

The dating of Chinese currency has evolved significantly, reflecting the nation's political transformations. All coinage issued by the People's Republic of China since its founding in 1949 has used the standard Gregorian calendar.16

Prior to 1949, coins of the Republic of China were dated according to the Republic of China calendar, which marks 1912 as Year 1\. The conversion to the Gregorian calendar is straightforward: Gregorian Year \= Republic Year \+ 1911\. This system remains in official use in Taiwan.16

Some machine-struck coins from the preceding Qing Dynasty employed the traditional sexagenary cycle. This is a 60-year lunar cycle where the year is designated by a pair of characters—one from a set of ten "heavenly stems" and one from twelve "earthly branches." Because the cycle repeats, converting these dates to the Gregorian calendar requires historical context to place the coin within the correct 60-year period.16

A critical challenge in cataloging Republican-era coinage is the phenomenon of the "frozen date." The need for vast quantities of coinage for commerce, particularly for popular designs like the Yuan Shikai "Fat Man" dollar, meant that mints often did not create new dies for each successive year. Instead, they continued using dies with a fixed date, such as "Year 3" (1914), for many years, with some production runs occurring as late as the 1950s.16 This means the date inscribed on the coin is not a reliable indicator of its actual year of mintage. For a database to be numismatically accurate, it must differentiate between the date depicted on the item and the true period of its manufacture. This requires fields for both

date\_on\_coin and actual\_mintage\_period, supplemented by notes on die varieties and restrikes that help pinpoint the production era. Simply cataloging all "Year 3" dollars as being from 1914 would be a significant numismatic oversimplification.

#### **1.5 Numismatic Edge Cases**

* **Hyperinflation (1940s):** The immense financial strain of the Second Sino-Japanese War and the Chinese Civil War led the Nationalist government to finance its deficits through the printing press, triggering one of the most severe hyperinflationary episodes in modern history.19 The initial currency, the  
  *fabi*, rapidly devalued. In a final effort to stabilize the economy in August 1948, the government introduced the Gold Yuan and forced citizens to exchange their gold and foreign currency for the new notes.21 This reform failed catastrophically. The currency collapsed, with denominations soaring into the millions. By May 1949, the price of a single grain of rice in Shanghai had surpassed 100 Gold Yuan.23 These banknotes are tangible artifacts of complete monetary collapse. An example identifier for a 5,000,000 Gold Yuan note from 1949 would be  
  CN-GY-1949-5M.  
* **Chinese Soviet Republic (1931-1937):** During the Chinese Civil War, the Chinese Communist Party established a government in the territories it controlled and issued its own distinct currency through the Chinese Soviet Republic National Bank.24 These issues included copper 5 Cent coins (1932), silver 20 Cent coins (1932-33), and silver 1 Yuan coins (1934), as well as a variety of banknotes.25 Featuring prominent communist iconography such as the hammer and sickle, these coins and notes represent a period of state-building in opposition to the Nationalist government and are a highly sought-after area of Chinese numismatics. An example identifier for a 20 Cent coin from 1932 would be  
  CN-CSR-1932-20C.  
* **Japanese Occupation (1930s-1940s):** As part of its invasion of China, Japan engaged in economic warfare by establishing puppet banks, such as the Mengchiang Bank, which issued their own regional currencies.27 These notes were designed to circulate alongside and undermine the national  
  *fabi* currency, disrupting the economy and asserting Japanese control. These issues are distinct from the more generic Japanese Invasion Money (JIM) used in other parts of Asia and represent a targeted use of currency as a weapon of war. An example identifier for a 5 Yuan note from a Japanese puppet bank in 1940 would be CN-JAPOCC-1940-5Y.

---

### **Chapter 2: Canada (CAD)**

#### **2.1 Foundational Data**

* **Country Code:** CA 28  
* **Country Name:** Canada. The formal, though now seldom used, title is the Dominion of Canada.30  
* **Market Priority:** 2

#### **2.2 Issuing Authorities: Mints and Printers**

The production of Canadian currency is divided between a government Crown corporation for coinage and a private company for banknotes. The Royal Canadian Mint (RCM) is responsible for all of Canada's circulation and numismatic coins.32 The RCM operates two facilities: its historic headquarters in Ottawa, opened in 1908, which handles collector coins, bullion, and master tooling; and a high-volume production facility in Winnipeg, opened in 1976, which strikes all Canadian circulation coins as well as coins for other nations.32

Since 1935, all Canadian banknotes have been produced under contract by the Canadian Bank Note Company (CBNC), a private security printing firm based in Ottawa.35 Historically, other firms such as the British American Bank Note Company also printed Canadian currency.37

The use of mint marks on Canadian coins has evolved to serve various functions. Early coins struck for Canada before the Ottawa mint's opening were sometimes produced at the Heaton Mint in England and bear an "H" mark.32 The first sovereigns produced in Ottawa used a "C" for Canada to establish a national identity.38 In the modern era, marks have diversified. A "W" is sometimes used on collector coins to denote production at the Winnipeg facility, creating a numismatic variety.39 A "P" mark indicates the coin's composition (plated steel) rather than its location.38 Most commonly, modern circulation coins feature the RCM's stylized maple leaf logo, which serves as a brand identifier for the mint as a whole. This progression shows a transformation of the mint mark from a simple indicator of origin to a multifaceted tool for branding, technical specification, and the creation of collectible varieties. For database purposes, this complexity necessitates separate fields for

mint\_mark, composition\_mark, and privy\_mark to avoid misclassification.

#### **2.3 Collectible Coin and Banknote Types**

The Canadian collector market is robust, with high interest in key-date coins, historical series, and famous varieties.

Among coins, the 1936 "Dot" coinage stands out as exceptionally desirable. These coins were struck in 1937 using 1936-dated dies to which a small dot was added, as new dies for King George VI were not yet ready. The 1936 Dot 1 Cent is a legendary rarity with only three known examples.40 Other key rarities include the 1921 50 Cents, known as the "King of Canadian coins" after most of the mintage was melted, and the 1911 Pattern Silver Dollar, of which only two silver examples are known.40 In the modern era, the RCM's Gold, Silver, and Platinum Maple Leaf bullion series are globally popular with both investors and collectors.

For banknotes, early government issues and special printings are highly sought after.41 Notes from the Dominion of Canada (1870-1923), particularly the fractional 25 Cent "shinplasters" and the large-format notes often called "horseblankets," are foundational to the hobby.43 The first series from the Bank of Canada (1935 and 1937\) are also very popular. A famous and highly collectible variety is the 1954 "Devil's Face" series, where an anomaly in the engraving of Queen Elizabeth II's hair creates the illusion of a devil's face. Additionally, "Star Notes," which have an asterisk preceding the serial number, were printed to replace faulty notes during production. Their low print runs make them much scarcer than regular issues and they command significant premiums.

#### **2.4 Dating Systems**

Canada has exclusively used the Gregorian calendar for all official coinage and banknotes since its inception. No special conversion is required for cataloging.

#### **2.5 Numismatic Edge Cases**

* **Colonial Tokens (pre-1867):** Before Confederation in 1867, the British North American colonies suffered from a chronic shortage of official coinage. To facilitate local commerce, a wide array of private and semi-official tokens were issued and circulated as money.45 These tokens are a foundational element of Canadian numismatics.  
  * **Description:** These tokens were a pragmatic response to the economic realities of the colonies, filling a monetary vacuum left by the imperial government. Prominent examples include the "Habitant" tokens of 1837, issued by Montreal banks for Lower Canada, which depicted a French-Canadian farmer and were authorized by the colonial government, making them "semi-regal" coinage.45 Other widely circulated series include the "Bouquet Sou" tokens of Lower Canada and various tokens issued by the Bank of Upper Canada.45 These issues demonstrate the development of distinct regional economic identities prior to the creation of a unified Dominion.  
  * **Example ID:** CA-LC-1837-TOKEN-HP (representing a Lower Canada Habitant Half Penny Token from 1837).

---

### **Chapter 3: Germany (DE)**

#### **3.1 Foundational Data**

* **Country Code:** DE 47  
* **Country Name:** Federal Republic of Germany (*Bundesrepublik Deutschland*).48  
* **Market Priority:** 3

#### **3.2 Issuing Authorities: Mints and Printers**

Germany's currency production infrastructure is a direct legacy of its 19th-century unification, characterized by a decentralized minting system and both state-owned and private banknote printing. Five active state mints produce the nation's coinage, each identified by a distinct mint mark 50:

* **A:** Staatliche Münze Berlin (State Mint of Berlin)  
* **D:** Bayerisches Hauptmünzamt (Bavarian Main Mint, Munich)  
* **F:** Staatliche Münzen Baden-Württemberg (Stuttgart)  
* **G:** Staatliche Münzen Baden-Württemberg (Karlsruhe)  
* **J:** Hamburgische Münze (Hamburg Mint)

This system reflects Germany's federal political structure. When the German Empire was formed in 1871, it consolidated eight different currency systems but allowed constituent states like Prussia, Bavaria, and Saxony to continue minting coins.52 The lettered mint marks were assigned based on the state's political importance in the Bundesrat (Federal Council), not by geography.52 This system has remained remarkably consistent through the German Empire, the Weimar Republic, the nation's division during the Cold War, and into the modern Euro era. This continuity underscores that the mint marks are not merely administrative identifiers but are deeply embedded symbols of Germany's federal identity.

Banknote production is handled by two main entities. The **Bundesdruckerei** (Federal Press) in Berlin is a state-owned enterprise with roots in the 19th-century Reichsdruckerei, producing Euro banknotes and other secure documents.54 Additionally,

**Giesecke+Devrient (G+D)**, a private company in Munich founded in 1852, is a major global player in security printing and produces banknotes for Germany and many other nations.56

#### **3.3 Collectible Coin and Banknote Types**

The German collector market is diverse, with strong interest in Imperial coinage, Weimar-era issues, and modern Euro commemoratives.

Coins of the German Empire (1871-1918) are highly collectible, particularly the silver Mark denominations (1, 2, 3, and 5 Mark) and gold Marks (5, 10, and 20 Mark). Because each state issued its own versions with the portrait of its respective monarch, collectors often specialize in a particular state, such as Prussia or Bavaria.58 Coins from the Weimar Republic (1919-1933), including silver Reichsmark issues and commemoratives like the "Goethe" 5 Mark, are also popular.60 In the modern era, the commemorative 2 Euro coins are widely collected, with many enthusiasts seeking to acquire a complete set of each design from all five mints (A, D, F, G, J).

German banknote collecting is often anchored by the historically significant hyperinflation notes of the Weimar Republic. Issued from 1922-1923, these notes reached denominations in the trillions of Marks and serve as a stark reminder of economic collapse.61 Although vast quantities were printed, making many of them affordable, they remain a cornerstone of historical currency collections. The Deutsche Mark notes issued by West Germany (1948-2002) are also popular, particularly the well-regarded designs of the third (1960s) and fourth (1990s) series.

#### **3.4 Dating Systems**

Germany uses the Gregorian calendar for all official coinage and banknotes. No conversion is needed for cataloging purposes.

#### **3.5 Numismatic Edge Cases**

* **Hyperinflation (Weimar Republic, 1922-1923):** Crippling war reparations from the Treaty of Versailles and soaring government debt plunged the Weimar Republic into one of history's most studied hyperinflationary spirals.63 The currency, known as the  
  *Papiermark*, became functionally worthless.  
  * **Description:** The government printed banknotes in a frantic attempt to keep pace with inflation, issuing notes with denominations that reached 100 Trillion Marks. The purchasing power of the currency evaporated; a loaf of bread that cost 160 Marks in late 1922 cost 200 Billion Marks by late 1923\.63 These notes are the quintessential example of hyperinflationary currency.  
  * **Example ID:** DE-WEIMAR-1923-100T (representing a 100 Trillion Mark note).  
* ***Notgeld*** **(Emergency Money):** During and immediately after World War I, a severe shortage of official coinage prompted thousands of municipalities, private companies, and local savings banks to issue their own emergency money, or *Notgeld*.65  
  * **Description:** *Notgeld* is a vast and varied field of numismatics. It was produced on numerous materials, including paper, porcelain, silk, leather, and even compressed coal dust. During the peak of hyperinflation in 1923, many issuers produced *Wertbeständige* ("fixed value") notes denominated in commodities (rye, wheat, wood) or pegged to the Gold Mark to provide a stable medium of exchange. Additionally, many towns issued colorful, illustrative series known as *Serienscheine*, which were intended for collectors from the outset and used to raise funds.66  
  * **Example ID:** DE-NOTGELD-BIELEFELD-1923-100B (representing a 100 Billion Mark note printed on linen, a form of *Stoffgeld*, from the city of Bielefeld).68  
* **Colonial Currency:** Germany issued distinct currencies for its colonial territories prior to their loss after World War I.  
  * **Description:** The most prominent example is the German East African Rupie, which circulated from 1890 to 1916\. Initially based on the Indian Rupee system (1 Rupie \= 64 Pesa), it was decimalized in 1904 to 1 Rupie \= 100 Heller and pegged to the German Mark at a rate of 15 Rupien to 20 Marks.70 Coins for the colony were struck at the Berlin ('A') and Hamburg ('J') mints, bearing the effigy of the German Emperor.71  
  * **Example ID:** DE-DOA-1904-1R (representing a 1 Rupie coin from German East Africa, dated 1904).

---

### **Chapter 4: Japan (JPY)**

#### **4.1 Foundational Data**

* **Country Code:** JP 73  
* **Country Name:** Japan. The official name is *Nippon-koku* or *Nihon-koku* (日本国).75  
* **Market Priority:** 4

#### **4.2 Issuing Authorities: Mints and Printers**

The production of Japanese currency is bifurcated between two specialized government institutions. Coinage is the exclusive responsibility of the Japan Mint, an Independent Administrative Institution established in 1871 during the Meiji Restoration to modernize the nation's currency.77 The Japan Mint operates its head office and primary facility in Osaka, with two additional branches in Saitama and Hiroshima.79 The Hiroshima branch was notably established in 1942 with the specific purpose of minting coins for occupied territories in Southeast Asia.79

All Japanese banknotes are manufactured by the National Printing Bureau (NPB), another incorporated administrative agency.82 The NPB operates its head office in Tokyo and maintains several production plants throughout the country, including facilities in Odawara, Shizuoka, and Hikone.82

Modern Japanese coins do not bear mint marks to distinguish their place of manufacture.85 This practice reflects a production philosophy centered on national uniformity, where the Japan Mint functions as a single, unified entity, and the specific origin of a coin is considered irrelevant for circulation. This approach contrasts with historical precedents. During the Meiji era, silver one-yen coins intended for foreign trade were counterstamped with the character "Gin" (銀, for silver) to prevent their re-importation after being sold overseas as bullion. The position of this mark designated the mint of origin: a mark on the left side of the reverse indicated the Osaka mint, while a mark on the right signified the Tokyo mint.86 Additionally, the very first modern yen coins for the Japanese government were struck at the San Francisco Mint in 1870, before the Osaka facility was fully operational.88

| facility\_name | location | mint\_mark | active\_period | produces |
| :---- | :---- | :---- | :---- | :---- |
| Japan Mint (Head Office) | Osaka | None | 1871-Present | \["coins", "medals"\] |
| Japan Mint (Saitama Branch) | Saitama | None | 1941-Present | \["coins", "medals"\] |
| Japan Mint (Hiroshima Branch) | Hiroshima | None | 1945-Present | \["coins", "medals"\] |
| San Francisco Mint (for Japan) | San Francisco, USA | S | 1870-1870 | \["coins"\] |
| Tokyo Mint (historical) | Tokyo | Gin (Right) | c. 1870s-1890s | \["coins"\] |
| Osaka Mint (historical) | Osaka | Gin (Left) | c. 1870s-1890s | \["coins"\] |
| National Printing Bureau | Tokyo (and others) | None | 1877-Present | \["banknotes", "stamps"\] |

#### **4.3 Collectible Coin and Banknote Types**

Collector interest in Japanese numismatics is strong across multiple historical eras, with a particular focus on the foundational issues of the modern currency system.

Key collectible coin types include the early denominations of the Meiji Era (1868-1912), such as the Rin, Sen, and the first silver and gold Yen coins. These pieces are fundamental to Japanese numismatics and command high collector interest.85 Coins from the subsequent Taishō (1912-1926) and early Shōwa (1926-1989) eras, especially issues from the wartime period, are also highly sought after. Modern circulating coinage generally has lower collector interest, with the exception of first or last years of issue and commemorative coins, which have a dedicated following.90

Among banknotes, early series from the Meiji and Taishō eras, such as the 1885 Daikokuten convertible notes, are highly valued for their rarity and historical importance.92 Notes from the immediate post-WWII period, particularly the "Series A" (1946-48) and "Series B" (1950-53) issues, are also highly collectible as they represent the country's recovery from war and hyperinflation.92 While modern circulating notes have limited appeal, commemorative issues like the 2000 Yen note, released for the Okinawa G8 Summit, have generated medium collector interest.93

#### **4.4 Dating Systems**

Japan employs the Japanese Era Name calendar, or *nengō* (年号), for dating its coinage, a system that is intrinsically linked to the reign of its emperors.94 With the ascension of a new emperor, a new era name is declared, and the year count resets to 1, known as

*gannen* (元年).95 The date on a coin is typically formatted as \[Era Name Kanji\] 年 (nen, for year).

Conversion to the Gregorian calendar is necessary for international cataloging and is calculated with the formula: Gregorian Year \= (Era Start Year \- 1\) \+ Reign Year. For example, for a coin dated Shōwa Year 45 (昭和四十五年), the calculation is (1926 \- 1\) \+ 45 \= 1970\.95

This system creates a significant data management challenge known as the "transition year" problem. An emperor's reign does not align with the Gregorian calendar, as an era officially ends and a new one begins on the day of succession. For instance, Emperor Hirohito passed away on January 7, 1989\. Consequently, coins dated Shōwa 64 were produced for the first seven days of 1989, while coins dated Heisei 1 were produced for the remainder of that year.95 This means a single Gregorian year can contain coins with two different era dates. A database schema must therefore include separate fields for

gregorian\_year, era\_name, and era\_year to maintain data integrity and allow for accurate queries.

| Era Name (Romaji) | Era Name (Kanji) | Start Date | End Date | Gregorian Offset |
| :---- | :---- | :---- | :---- | :---- |
| Meiji | 明治 | 1868-10-23 | 1912-07-30 | \+1867 |
| Taishō | 大正 | 1912-07-30 | 1926-12-25 | \+1911 |
| Shōwa | 昭和 | 1926-12-25 | 1989-01-07 | \+1925 |
| Heisei | 平成 | 1989-01-08 | 2019-04-30 | \+1988 |
| Reiwa | 令和 | 2019-05-01 | Present | \+2018 |

#### **4.5 Numismatic Edge Cases**

* **Hyperinflation (Post-WWII):** In the aftermath of World War II, Japan's economy was devastated, leading to a severe debt crisis and rampant hyperinflation that rendered the yen's pre-war value meaningless.88 This economic chaos necessitated the issuance of new, often lower-quality, banknotes and coins. The "Series A" banknotes of 1946-1948 are a direct product of this period and are highly collectible.92 The inflationary pressures made the sen and rin subsidiary units practically worthless, leading to their official demonetization in 1953\.88  
* **Colonial and Occupation Currency:** During its imperial expansion in the first half of the 20th century, Japan used currency as an explicit instrument of geopolitical control. Rather than using its domestic yen, it issued bespoke currencies for the territories it occupied. These issues, officially known as Southern Development Bank Notes or Japanese Invasion Money (JIM), were fiat currencies with no backing, designed to replace local currencies and extract economic value.98 This strategy severed the economic ties of occupied nations to their former colonial powers and asserted Japanese economic dominance as part of the "Greater East Asia Co-Prosperity Sphere".100  
  * **Korean Yen:** During the colonization of Korea (1910-1945), the local currency was replaced by the Korean yen, issued by the Japanese-controlled Bank of Chōsen and pegged to the Japanese yen.101  
  * **Japanese Invasion Money (JIM):** In territories like Malaya and the Philippines, Japan issued notes denominated in local units (dollars, pesos) to supplant the existing currency. These notes often had block letters indicating their intended region of use ('M' for Malaya) and became colloquially known as "Banana Money" in Malaya due to their design.103 They were declared worthless after the war.98  
* **Private and Local Currency:** Before the full centralization of currency under the Meiji government, Japan had a long history of local and private currency issuance.  
  * ***Hansatsu*** **(藩札):** Throughout the Edo period (1603-1867), feudal domains (*han*) issued their own paper money called *hansatsu*, which was typically valid only within that domain.88  
  * **National Bank Notes:** From 1872 to 1879, the government authorized a system of 153 private "national banks" to issue their own banknotes, a system that was abolished with the creation of the central Bank of Japan in 1882\.88

---

### **Chapter 5: Australia (AUD)**

#### **5.1 Foundational Data**

* **Country Code:** AU 107  
* **Country Name:** Commonwealth of Australia.109  
* **Market Priority:** 5

#### **5.2 Issuing Authorities: Mints and Printers**

Australia's modern currency production is handled by two principal government-owned entities. All of the nation's circulating coinage is produced by the **Royal Australian Mint** in Canberra. Opened in 1965, it was the first Australian mint to operate independently of the British Royal Mint. For its collector and uncirculated coin programs, it sometimes uses a 'C' mint mark for Canberra, though this is often absent on standard circulating coins.111

The **Perth Mint**, originally established in 1899 as a branch of the British Royal Mint, now focuses primarily on producing Australia's world-renowned bullion coins (such as the Gold Kangaroo and Silver Kookaburra series) and other numismatic products. Its coins are identifiable by a 'P' mint mark.112 Historically, coins for Australia were also struck at the now-defunct Sydney Mint (1855-1926, mint mark 'S') and Melbourne Mint (1872-1967, mint mark 'M').111

All Australian banknotes are produced by **Note Printing Australia (NPA)**. Located in Craigieburn, a suburb of Melbourne, the NPA is a wholly-owned subsidiary of the Reserve Bank of Australia. It is globally recognized as a pioneer of polymer banknote technology, having introduced the world's first polymer note in 1988\.114

#### **5.3 Collectible Coin and Banknote Types**

The Australian numismatic market shows strong interest in key-date pre-decimal coins, modern bullion issues, and early paper currency.

Among pre-decimal coinage (1910-1964), certain dates are highly valuable due to low mintage numbers, such as the 1930 Penny and the 1923 Halfpenny.116 Gold Sovereigns struck at the Sydney, Melbourne, and Perth mints are also a cornerstone of historical Australian collecting. In the modern era, the various bullion series from the Perth Mint—including the Gold Kangaroo, Silver Kookaburra, Silver Koala, and the annual Lunar series—have a large and active international collector base.116

For banknotes, issues from the pre-decimal era (1913-1966) are highly sought after, especially higher denominations like the £5 and £10 notes, and those bearing the signatures of Riddle and Sheehan.118 Similar to Canada, Australia used "Star Notes" as replacement notes for sheets spoiled during production. These notes, identifiable by a star in the serial number, were printed in much smaller quantities than regular issues and command significant premiums from collectors.118 The 1988 commemorative $10 banknote is also of high interest as it was the world's first circulating polymer banknote, a major technological innovation in currency.114

#### **5.4 Dating Systems**

Australia uses the Gregorian calendar for all official coinage and banknotes. No conversion is needed for cataloging.

#### **5.5 Numismatic Edge Cases**

* **Colonial Currency (Holey Dollar and Dump):** In 1813, to address a severe currency shortage in the colony of New South Wales, Governor Lachlan Macquarie authorized a creative solution. He had the centers punched out of 40,000 imported Spanish Silver Dollars.119  
  * **Description:** This process created two new coins from one. The outer ring was counterstamped with "NEW SOUTH WALES 1813" and given a value of Five Shillings, becoming known as the "Holey Dollar." The center plug, or "Dump," was counterstamped with a crown and valued at Fifteen Pence. This act created Australia's first distinct currency, designed specifically to remain within the colony. The coins were demonetized in 1829, and very few survive today.  
  * **Example ID:** AU-NSW-1813-HD (Holey Dollar).  
* **Adelaide Pound (Gold Tokens):** An economic crisis in the Colony of South Australia, sparked by the Victorian gold rush draining the colony of currency, led the Government Assay Office in Adelaide to strike gold tokens in 1852\.121  
  * **Description:** This was technically an illegal act, as the colony did not have British approval to mint its own currency. The office produced gold pieces in denominations of £1, £2, and £5. The initial die for the £1 piece, known as the Adelaide Pound Type I, cracked almost immediately, making the few surviving examples extremely rare. Furthermore, the coins contained more gold than their face value, leading many to be melted down for profit, which has compounded their rarity today.  
  * **Example ID:** AU-SA-1852-AP1 (Adelaide Pound Type I).

---

### **Chapter 6: Russia (RUB)**

#### **6.1 Foundational Data**

* **Country Code:** RU 123  
* **Country Name:** Russian Federation (*Rossiyskaya Federatsiya*). The name Russia is considered equipollent.125  
* **Market Priority:** 6

#### **6.2 Issuing Authorities: Mints and Printers**

Currency production in Russia is managed by Goznak, a state-owned joint-stock company responsible for manufacturing banknotes, coins, stamps, and other secure documents.127 Goznak operates two major mints:

* **Moscow Mint (MMD):** Re-established in 1942, the Moscow Mint produces coins, medals, and decorations, including coins for foreign countries. Its mint mark is ММД or M.129  
* **Saint Petersburg Mint (SPMD):** Founded by Peter the Great in 1724, it is one of the oldest mints in the world. Its mint mark is СПМД, СП, or С-П.130

Banknote printing is also handled by Goznak, which incorporates several printing factories and paper mills, including facilities in Moscow and Perm.128 Historically, the Saint Petersburg Mint was known as the Leningrad Mint during the Soviet era (1924-1995) and used the ЛМД mint mark.131

#### **6.3 Collectible Coin and Banknote Types**

The Russian numismatic market is rich with highly collectible items from the Imperial, Soviet, and modern eras.

Imperial Russian coins (pre-1917) are extremely popular, with large silver Roubles and copper 5 Kopek coins from the reign of Catherine the Great being particularly sought after.132 Gold 5 and 10 Rouble coins of Nicholas II are also foundational to the market. Early Soviet Union coinage (1921-1950s) has a strong collector base, especially key dates and low-mintage issues.

Russian banknotes offer a wide field for collectors. Imperial-era State Credit Notes, particularly the large-format notes with portraits of Tsars, are highly valued.134 Banknotes from the Russian Civil War period (c. 1918-1922) are also of great interest, with numerous issues from various regional governments (e.g., South Russia, Siberia). Modern Russian commemorative banknotes, such as the 2014 Sochi Olympics 100 Rouble note and the 2018 FIFA World Cup 100 Rouble note, have proven popular with international collectors.

#### **6.4 Dating Systems**

Russia uses the Gregorian calendar for all modern coinage and banknotes. No conversion is needed.

#### **6.5 Numismatic Edge Cases**

* **Hyperinflation (Early 1920s and 1990s):** Russia has experienced two major hyperinflationary periods.  
  * **Early 1920s:** Following the Russian Revolution and Civil War, the Soviet government printed vast quantities of currency (*Sovznaki*), leading to hyperinflation. Denominations reached as high as 100,000 roubles before the currency was reformed.136  
  * **Early 1990s:** The dissolution of the Soviet Union in 1991 led to a period of severe economic disruption and hyperinflation. The Central Bank of Russia issued banknotes in rapidly increasing denominations, culminating in a 500,000 Rouble note in 1997 before the currency was redenominated in 1998 at a rate of 1000 to 1\.137  
  * **Example ID:** RU-RF-1997-500K (representing a 500,000 Rouble note from 1997).  
* **Siberian Coinage (1764-1779):** During the reign of Catherine the Great, a special regional coinage was struck for use in Siberia.  
  * **Description:** These copper coins were minted at the Suzun Mint from locally mined copper that contained trace amounts of gold and silver, giving them a slightly higher intrinsic value than standard imperial copper. They feature a distinct design with two sables supporting a crowned cartouche and the inscription "Siberian Coin" (СИБИРСКАЯ МОНЕТА).139 Denominations included the Polushka, Denga, Kopek, 2, 5, and 10 Kopeks.  
  * **Example ID:** RU-SIB-1768-10K (representing a 10 Kopek Siberian coin from 1768).

---

### **Chapter 7: Mexico (MXN)**

#### **7.1 Foundational Data**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **7.2 Issuing Authorities: Mints and Printers**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **7.3 Collectible Coin and Banknote Types**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **7.4 Dating Systems**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **7.5 Numismatic Edge Cases**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

---

### **Chapter 8: South Africa (ZAR)**

#### **8.1 Foundational Data**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **8.2 Issuing Authorities: Mints and Printers**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **8.3 Collectible Coin and Banknote Types**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **8.4 Dating Systems**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **8.5 Numismatic Edge Cases**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

---

### **Chapter 9: Great Britain (GBP)**

#### **9.1 Foundational Data**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **9.2 Issuing Authorities: Mints and Printers**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **9.3 Collectible Coin and Banknote Types**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **9.4 Dating Systems**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **9.5 Numismatic Edge Cases**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

---

### **Chapter 10: France (FRF/EUR)**

#### **10.1 Foundational Data**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **10.2 Issuing Authorities: Mints and Printers**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **10.3 Collectible Coin and Banknote Types**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **10.4 Dating Systems**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

#### **10.5 Numismatic Edge Cases**

Data for this section was not available in the provided research materials. A dedicated research task is recommended to collect this information.

---

## **Part II: Synthesis and Strategic Recommendations**

### **11.1 Cross-Cutting Themes in Numismatic Data**

The detailed analysis of the six primary collector markets reveals several recurring themes that are critical for designing a robust and accurate numismatic database.

First, geopolitical instability consistently acts as a catalyst for the creation of numismatically significant "edge case" currencies. The hyperinflationary banknotes of Weimar Germany and 1940s China, the emergency *Notgeld* issues, the currency of the Chinese Soviet Republic, Japan's various Invasion Monies, and Russia's post-Soviet hyperinflationary notes are all direct consequences of war, revolution, or state failure. These are not mere anomalies but predictable numismatic responses to crisis. A database architecture must therefore be inherently flexible, capable of handling non-state issuers (such as municipalities or revolutionary movements), unconventional denominations, and non-standard materials beyond metal and paper.

Second, the function and form of mint marks are not universal but reflect distinct national philosophies of governance and production. Germany's enduring system of lettered mints is a direct reflection of its federal political structure. Canada's use of mint marks has evolved from a simple indicator of origin to a complex tool for branding, technical specification (e.g., plated composition), and the deliberate creation of collectible varieties. In contrast, modern Japan and China have largely abandoned mint marks in favor of a philosophy of national uniformity. This variety shows that mint marks are a rich data source encoding political, technical, and commercial information; treating them as a simple location string in a database would be a significant oversimplification.

Third, non-standard dating systems present a major technical challenge for data integrity. The Japanese era-name calendar and the pre-1949 Chinese Republican and sexagenary cycle calendars are not merely alternative systems; they are deeply tied to political and dynastic legitimacy. The "transition year" problem in Japan (where two era-dates can exist in one Gregorian year) and the "frozen date" problem in Republican China (where a single date was used for decades of production) are critical data integrity challenges that must be addressed at the schema level to prevent erroneous cataloging.

### **11.2 Database Schema Recommendations**

Based on the preceding analysis, the following recommendations are proposed for the database schema to ensure accuracy, flexibility, and numismatic integrity:

* **Issuers Table:** A flexible issuers table is paramount. It should include an issuer\_type field with a controlled vocabulary (e.g., 'Federal Government', 'State Mint', 'Puppet Bank', 'Colonial Authority', 'Private Bank', 'Municipality'). This structure will allow for the accurate cataloging of the full spectrum of issuing authorities, from the Bank of Canada to a small German town issuing porcelain *Notgeld*.  
* **Coin and Banknote Tables:**  
  * To handle complex dating, separate fields for date\_on\_item (as a string) and gregorian\_year (as an integer) are essential. This accommodates non-Gregorian dates while enabling standardized sorting and searching.  
  * To capture the nuanced use of marks, separate, nullable fields for mint\_mark, privy\_mark, and composition\_mark should be created to prevent misclassification and data loss.  
  * A dedicated series field (e.g., "Series A," "1954 Devil's Face") is crucial for banknotes, as collector interest is often series-driven.  
  * A boolean field, is\_replacement\_note, is necessary to properly identify and catalog "star notes" from Canada, Australia, and other Commonwealth nations.  
* **Edge Case Linkage:** A relational table should be implemented to link edge case currencies to the primary issuing authority. For instance, a Japanese Invasion Money note issued for use in the Philippines would link to "Japan" in the issuers table but would have "Philippines" in a territory\_of\_use field. This model correctly attributes issuance while capturing the specific context of the currency's circulation.

### **11.3 Future Priorities and Data Validation**

The initial data collection has revealed significant gaps for four of the ten priority countries: Mexico, South Africa, Great Britain, and France. A dedicated research phase to gather the required data for these markets is the immediate next priority. Based on global market trends and numismatic complexity, future expansion of the database should consider adding India (with its complex Moghul, Princely State, and British colonial issues), Brazil (a history of multiple currency reforms), and Italy (diverse pre-unification state coinage).

For ongoing data validation and enrichment, a strategy of continuous cross-referencing with major auction house archives (e.g., Heritage, Stack's Bowers) and integrating population report data from major grading services (PCGS, NGC, PMG) is recommended. This will provide real-world data on rarity, condition, and market demand, allowing for the collector\_interest field to be a dynamic, data-driven metric rather than a static assessment.

#### **Works cited**

1. en.wikipedia.org, accessed July 31, 2025, [https://en.wikipedia.org/wiki/ISO\_3166-2:CN](https://en.wikipedia.org/wiki/ISO_3166-2:CN)  
2. ISO 3166-1 alpha-2 country code: CN \- Localizely, accessed July 31, 2025, [https://localizely.com/country-code/CN/](https://localizely.com/country-code/CN/)  
3. China Background \- Clinton White House, accessed July 31, 2025, [https://clintonwhitehouse4.archives.gov/WH/New/China/china.html](https://clintonwhitehouse4.archives.gov/WH/New/China/china.html)  
4. China \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/China](https://en.wikipedia.org/wiki/China)  
5. China Banknote Printing and Minting Corporation \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/China\_Banknote\_Printing\_and\_Minting\_Corporation](https://en.wikipedia.org/wiki/China_Banknote_Printing_and_Minting_Corporation)  
6. CBPM, accessed July 31, 2025, [https://www.cbpm.cn/en/](https://www.cbpm.cn/en/)  
7. Learn the History of the Chinese Mint | Provident, accessed July 31, 2025, [https://www.providentmetals.com/knowledge-center/collectible-coins/chinese-mint-history.html](https://www.providentmetals.com/knowledge-center/collectible-coins/chinese-mint-history.html)  
8. en.wikipedia.org, accessed July 31, 2025, [https://en.wikipedia.org/wiki/China\_Banknote\_Printing\_and\_Minting\_Corporation\#:\~:text=Banknote%20printing%20facilities%20are%20located,an%2C%20Shijiazhuang%2C%20and%20Nanchang.](https://en.wikipedia.org/wiki/China_Banknote_Printing_and_Minting_Corporation#:~:text=Banknote%20printing%20facilities%20are%20located,an%2C%20Shijiazhuang%2C%20and%20Nanchang.)  
9. An introduction and identification guide to Chinese Qing-dynasty coins | Lincoln Museum, accessed July 31, 2025, [https://www.lincolnmuseum.com/assets/downloads/An\_introduction\_and\_identification\_guide\_to\_Chinese\_Qing\_dynasty\_coins.pdf](https://www.lincolnmuseum.com/assets/downloads/An_introduction_and_identification_guide_to_Chinese_Qing_dynasty_coins.pdf)  
10. Banknote Printers by Country or Region \- Best of Banknotes, accessed July 31, 2025, [https://www.bestofbanknotes.com/banknote-printers-by-country-or-region/](https://www.bestofbanknotes.com/banknote-printers-by-country-or-region/)  
11. Price Guide: China \- PCGS Asia, accessed July 31, 2025, [https://www.pcgsasia.com/price/chinesecoins](https://www.pcgsasia.com/price/chinesecoins)  
12. PCGS Chinese Coin Price Guide, accessed July 31, 2025, [https://www.pcgs.com/prices/china](https://www.pcgs.com/prices/china)  
13. Top 25 Most Commonly Counterfeited Chinese Coins | NGC, accessed July 31, 2025, [https://www.ngccoin.uk/resources/counterfeit-detection/top/chinese/](https://www.ngccoin.uk/resources/counterfeit-detection/top/chinese/)  
14. The Top 10 Chinese Banknotes According to the PMG Population Report, accessed July 31, 2025, [https://www.pmgnotes.com/news/article/5450/The-Top-10-Chinese-Banknotes-According-to-the-PMG-Population-Report/](https://www.pmgnotes.com/news/article/5450/The-Top-10-Chinese-Banknotes-According-to-the-PMG-Population-Report/)  
15. The Hsu Collection of Chinese Banknotes \- Full List \- PMG, accessed July 31, 2025, [https://www.pmgnotes.com/gallery/hsu/all/](https://www.pmgnotes.com/gallery/hsu/all/)  
16. Chinese Coin Dating Systems \- PCGS, accessed July 31, 2025, [https://www.pcgs.com/news/chinese-coin-dating-systems](https://www.pcgs.com/news/chinese-coin-dating-systems)  
17. How to convert a Chinese date \- My China Roots, accessed July 31, 2025, [https://www.mychinaroots.com/wiki/article/how-to-convert-a-chinese-date](https://www.mychinaroots.com/wiki/article/how-to-convert-a-chinese-date)  
18. What dating system did the Chinese use prior to adopting the Western/Christian system, and when and why did they change systems? : r/AskHistorians \- Reddit, accessed July 31, 2025, [https://www.reddit.com/r/AskHistorians/comments/5q5z7f/what\_dating\_system\_did\_the\_chinese\_use\_prior\_to/](https://www.reddit.com/r/AskHistorians/comments/5q5z7f/what_dating_system_did_the_chinese_use_prior_to/)  
19. Chinese hyperinflation \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Chinese\_hyperinflation](https://en.wikipedia.org/wiki/Chinese_hyperinflation)  
20. Hyperinflation \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Hyperinflation](https://en.wikipedia.org/wiki/Hyperinflation)  
21. History of Chinese currency \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/History\_of\_Chinese\_currency](https://en.wikipedia.org/wiki/History_of_Chinese_currency)  
22. Gold Yuan Notes \- Mainland China Period \- 中央銀行 券幣數位博物館, accessed July 31, 2025, [https://museum.cbc.gov.tw/web/en-us/history/introduce/mainland/gold](https://museum.cbc.gov.tw/web/en-us/history/introduce/mainland/gold)  
23. "One Hundred Yuan for A Grain" \- Grave Impact of Galloping Inflation (1946 \- 1949), accessed July 31, 2025, [https://www.boc.cn/en/aboutboc/ab7/200809/t20080926\_1601861.html](https://www.boc.cn/en/aboutboc/ab7/200809/t20080926_1601861.html)  
24. Chinese Soviet Republic National Bank \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Chinese\_Soviet\_Republic\_National\_Bank](https://en.wikipedia.org/wiki/Chinese_Soviet_Republic_National_Bank)  
25. Chinese Soviet Republic | eBay, accessed July 31, 2025, [https://www.ebay.com/shop/chinese-soviet-republic?\_nkw=chinese+soviet+republic](https://www.ebay.com/shop/chinese-soviet-republic?_nkw=chinese+soviet+republic)  
26. China \- Early Soviet CHINESE SOVIET REPUBLIC 5 Cents Y 507 Prices & Va \- NGC, accessed July 31, 2025, [https://www.ngccoin.com/price-guide/world/china-early-soviet-chinese-soviet-republic-5-cents-y-507-ca.1932-cuid-1045755-duid-1288947](https://www.ngccoin.com/price-guide/world/china-early-soviet-chinese-soviet-republic-5-cents-y-507-ca.1932-cuid-1045755-duid-1288947)  
27. INFLATION IN EASTERN CHINA DURING THE SECOND SINO-JAPANESE WAR \- Studies in Applied Economics \- Johns Hopkins University, accessed July 31, 2025, [https://sites.krieger.jhu.edu/iae/files/2020/01/Inflation-in-Eastern-China-during-the-Second-Sino-Japanese-War.pdf](https://sites.krieger.jhu.edu/iae/files/2020/01/Inflation-in-Eastern-China-during-the-Second-Sino-Japanese-War.pdf)  
28. en.wikipedia.org, accessed July 31, 2025, [https://en.wikipedia.org/wiki/ISO\_3166-2:CA\#:\~:text=The%20first%20part%20is%20CA,for%20the%20province%20or%20territory.](https://en.wikipedia.org/wiki/ISO_3166-2:CA#:~:text=The%20first%20part%20is%20CA,for%20the%20province%20or%20territory.)  
29. ISO 3166-2:CA \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/ISO\_3166-2:CA](https://en.wikipedia.org/wiki/ISO_3166-2:CA)  
30. en.wikipedia.org, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Name\_of\_Canada\#:\~:text=Upon%20Confederation%20in%201867%2C%20Canada,%22Realm%20of%20the%20Commonwealth%22.](https://en.wikipedia.org/wiki/Name_of_Canada#:~:text=Upon%20Confederation%20in%201867%2C%20Canada,%22Realm%20of%20the%20Commonwealth%22.)  
31. Dominion of Canada | The Canadian Encyclopedia, accessed July 31, 2025, [https://www.thecanadianencyclopedia.ca/en/article/dominion](https://www.thecanadianencyclopedia.ca/en/article/dominion)  
32. Complete Guide to the Royal Canadian Mint \- GovMint.com, accessed July 31, 2025, [https://www.govmint.com/coin-authority/post/complete-guide-to-the-royal-canadian-mint](https://www.govmint.com/coin-authority/post/complete-guide-to-the-royal-canadian-mint)  
33. FAQ | The Royal Canadian Mint, accessed July 31, 2025, [https://www.mint.ca/en/faq](https://www.mint.ca/en/faq)  
34. Visit the Mint | The Royal Canadian Mint, accessed July 31, 2025, [https://www.mint.ca/en/visit-the-mint](https://www.mint.ca/en/visit-the-mint)  
35. Canadian Bank Note Company \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Canadian\_Bank\_Note\_Company](https://en.wikipedia.org/wiki/Canadian_Bank_Note_Company)  
36. Banknotes of the Canadian dollar \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Banknotes\_of\_the\_Canadian\_dollar](https://en.wikipedia.org/wiki/Banknotes_of_the_Canadian_dollar)  
37. List of banknote printers \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/List\_of\_banknote\_printers](https://en.wikipedia.org/wiki/List_of_banknote_printers)  
38. Canada: mints and mint marks? General for all denominations. \- Numista, accessed July 31, 2025, [https://en.numista.com/forum/topic120116.html](https://en.numista.com/forum/topic120116.html)  
39. Canadian Circulation Coin Mintage Quantities \- Saskatoon Coin Club, accessed July 31, 2025, [https://www.saskatooncoinclub.ca/articles/02\_coin\_mintages.html](https://www.saskatooncoinclub.ca/articles/02_coin_mintages.html)  
40. Rare Canadian Coins \- Saskatoon Coin Club, accessed July 31, 2025, [https://www.saskatooncoinclub.ca/articles/11\_rare\_canadian\_coins.html](https://www.saskatooncoinclub.ca/articles/11_rare_canadian_coins.html)  
41. Certified Banknotes \- MK Coins, accessed July 31, 2025, [https://mkcoins.com/collections/certified-banknotes](https://mkcoins.com/collections/certified-banknotes)  
42. Canada's banknotes \- The banknote Numizon catalog, accessed July 31, 2025, [https://www.numizon.com/en/catalog/north-america/canadas-banknotes/](https://www.numizon.com/en/catalog/north-america/canadas-banknotes/)  
43. Canadian Bills \- Maple Ridge Museum, accessed July 31, 2025, [https://mapleridgemuseum.org/canadian-bills/](https://mapleridgemuseum.org/canadian-bills/)  
44. Dominion of Canada (1870-1872) \- The banknote Numizon catalog, accessed July 31, 2025, [https://www.numizon.com/en/catalog/north-america/canadas-banknotes/dominion-of-canada-1870-1872/](https://www.numizon.com/en/catalog/north-america/canadas-banknotes/dominion-of-canada-1870-1872/)  
45. Habitant token \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Habitant\_token](https://en.wikipedia.org/wiki/Habitant_token)  
46. Canadian Tokens (1820-1860) for sale \- eBay, accessed July 31, 2025, [https://www.ebay.com/b/Canadian-Tokens-1820-1860/149940/bn\_2310858](https://www.ebay.com/b/Canadian-Tokens-1820-1860/149940/bn_2310858)  
47. opencagedata.com, accessed July 31, 2025, [https://opencagedata.com/guides/how-to-determine-the-iso-codes-for-a-location](https://opencagedata.com/guides/how-to-determine-the-iso-codes-for-a-location)  
48. en.wikipedia.org, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Names\_of\_Germany](https://en.wikipedia.org/wiki/Names_of_Germany)  
49. Germany \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Germany](https://en.wikipedia.org/wiki/Germany)  
50. German Mint: The History and Popular Coins \- Provident Metals, accessed July 31, 2025, [https://www.providentmetals.com/knowledge-center/collectible-coins/german-mint-history.html](https://www.providentmetals.com/knowledge-center/collectible-coins/german-mint-history.html)  
51. In focus: Minting sites in Germany \- INORCOAT, accessed July 31, 2025, [https://inorcoat.com/en/in-focus-minting-sites-in-germany/](https://inorcoat.com/en/in-focus-minting-sites-in-germany/)  
52. Germany's mint marks are A, D, F, G, and J. What about the other letters? \- ColeMone, accessed July 31, 2025, [https://coleccionismodemonedas.com/en/mint-marks-germany/](https://coleccionismodemonedas.com/en/mint-marks-germany/)  
53. German Coinage Act \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/German\_Coinage\_Act](https://en.wikipedia.org/wiki/German_Coinage_Act)  
54. Banknote printing: Tradition forges trust \- Bundesdruckerei GmbH, accessed July 31, 2025, [https://www.bundesdruckerei-gmbh.de/en/solutions/banknote-printing](https://www.bundesdruckerei-gmbh.de/en/solutions/banknote-printing)  
55. Bundesdruckerei \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Bundesdruckerei](https://en.wikipedia.org/wiki/Bundesdruckerei)  
56. Private printing works \- Bavarikon, accessed July 31, 2025, [https://www.bavarikon.de/object/bav:BSB-CMS-0000000000006009?lang=en](https://www.bavarikon.de/object/bav:BSB-CMS-0000000000006009?lang=en)  
57. Banknote printing: innovative and trusted | G+D \- Giesecke+Devrient, accessed July 31, 2025, [https://www.gi-de.com/en/currency-technology/banknote-solutions/banknote-production/banknote-printing](https://www.gi-de.com/en/currency-technology/banknote-solutions/banknote-production/banknote-printing)  
58. German Rare Coins \- American Rarities, accessed July 31, 2025, [https://americanrarities.com/german-rare-coins/](https://americanrarities.com/german-rare-coins/)  
59. List of silver coins of the German Empire \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/List\_of\_silver\_coins\_of\_the\_German\_Empire](https://en.wikipedia.org/wiki/List_of_silver_coins_of_the_German_Empire)  
60. Rare German Coin Prices – Buy, Sell or Appraise Coins from ..., accessed July 31, 2025, [https://coins.ha.com/world-coins-index/germany.s?id=11](https://coins.ha.com/world-coins-index/germany.s?id=11)  
61. Deutsche Mark \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Deutsche\_Mark](https://en.wikipedia.org/wiki/Deutsche_Mark)  
62. Germany Currency And Banknotes For Sale, accessed July 31, 2025, [https://www.banknoteworld.com/banknotes/Banknotes-by-Country/Germany-Currency/](https://www.banknoteworld.com/banknotes/Banknotes-by-Country/Germany-Currency/)  
63. Weimar Germany Inflation Collection (Seven Bills) \- 1923 \- History Hoard, accessed July 31, 2025, [https://www.historyhoard.com/products/weimar-germany-inflation-collection-seven-bills-1920s-weimar-republic](https://www.historyhoard.com/products/weimar-germany-inflation-collection-seven-bills-1920s-weimar-republic)  
64. Hyperinflation in the Weimar Republic \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Hyperinflation\_in\_the\_Weimar\_Republic](https://en.wikipedia.org/wiki/Hyperinflation_in_the_Weimar_Republic)  
65. German Notgeld \- National Numismatic Collection Instructions (NMAH), accessed July 31, 2025, [https://transcription.si.edu/germannotgeld](https://transcription.si.edu/germannotgeld)  
66. Notgeld \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Notgeld](https://en.wikipedia.org/wiki/Notgeld)  
67. Notgeld.com, accessed July 31, 2025, [https://notgeld.com/](https://notgeld.com/)  
68. 10,000 Mark Note, Bielefeld, Germany, 1923 | National Museum of American History, accessed July 31, 2025, [https://americanhistory.si.edu/collections/nmah\_1342294](https://americanhistory.si.edu/collections/nmah_1342294)  
69. BIELEFELD 1923 LINEN\! 100 Milliarden \= 100 Billion Mark Inflation Notgeld Stoffgeld Germany, accessed July 31, 2025, [https://www.worldbanknotemarket.com/products/bielefeld-1923-linen-100-milliarden-100-billion-mark-inflation-notgeld-stoffgeld-germany](https://www.worldbanknotemarket.com/products/bielefeld-1923-linen-100-milliarden-100-billion-mark-inflation-notgeld-stoffgeld-germany)  
70. German East African rupie \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/German\_East\_African\_rupie](https://en.wikipedia.org/wiki/German_East_African_rupie)  
71. 1 Rupie \- Wilhelm II \- German East Africa \- Numista, accessed July 31, 2025, [https://en.numista.com/catalogue/pieces11914.html](https://en.numista.com/catalogue/pieces11914.html)  
72. German East Africa Rupie KM 10 Prices & Values \- NGC, accessed July 31, 2025, [https://www.ngccoin.com/price-guide/world/german-east-africa-rupie-km-10-1904-1914-cuid-1128680-duid-1333642](https://www.ngccoin.com/price-guide/world/german-east-africa-rupie-km-10-1904-1914-cuid-1128680-duid-1333642)  
73. ISO 3166-1 alpha-2 country code: JP \- Localizely, accessed July 31, 2025, [https://localizely.com/country-code/JP/](https://localizely.com/country-code/JP/)  
74. ISO 3166-1 alpha-2 \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/ISO\_3166-1\_alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)  
75. Japan \- IMUNA | NHSMUN | Model UN, accessed July 31, 2025, [https://imuna.org/resources/country-profiles/japan/](https://imuna.org/resources/country-profiles/japan/)  
76. Names of Japan \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Names\_of\_Japan](https://en.wikipedia.org/wiki/Names_of_Japan)  
77. History of Japanese Coins \- 造幣局, accessed July 31, 2025, [https://www.mint.go.jp/eng/kids-eng/eng\_kids\_history.html](https://www.mint.go.jp/eng/kids-eng/eng_kids_history.html)  
78. Japan Mint \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Japan\_Mint](https://en.wikipedia.org/wiki/Japan_Mint)  
79. English \- 造幣局, accessed July 31, 2025, [https://www.mint.go.jp/eng/](https://www.mint.go.jp/eng/)  
80. Coins Presently Minted \- 造幣局, accessed July 31, 2025, [https://www.mint.go.jp/eng/operations-eng/production-eng/production-aproach-eng/eng\_operations\_coin\_index.html](https://www.mint.go.jp/eng/operations-eng/production-eng/production-aproach-eng/eng_operations_coin_index.html)  
81. History of Branches \- 造幣局, accessed July 31, 2025, [https://www.mint.go.jp/eng/profile-eng/eng\_guide\_branches.html](https://www.mint.go.jp/eng/profile-eng/eng_guide_branches.html)  
82. National Printing Bureau \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/National\_Printing\_Bureau](https://en.wikipedia.org/wiki/National_Printing_Bureau)  
83. Who manufactures Japanese banknotes? : 日本銀行 Bank of Japan, accessed July 31, 2025, [https://www.boj.or.jp/en/about/education/oshiete/money/c01.htm](https://www.boj.or.jp/en/about/education/oshiete/money/c01.htm)  
84. National Printing Bureau | MOF-Navi \- Site for application for tour of facilities related to the Ministry of Finance, accessed July 31, 2025, [https://www.mof.go.jp/english/public\_relations/kengaku/npb.html](https://www.mof.go.jp/english/public_relations/kengaku/npb.html)  
85. English \- 造幣局, accessed July 31, 2025, [https://www.mint.go.jp/eng](https://www.mint.go.jp/eng)  
86. Japan Type Set \#7460 Meiji, 1 yen, gin left, 1870-1896 \- NGC Collectors Society, accessed July 31, 2025, [https://coins.www.collectors-society.com/wcm/coinview.aspx?sc=291257](https://coins.www.collectors-society.com/wcm/coinview.aspx?sc=291257)  
87. Collecting Japanese Silver Yen: The Dragon Yen 1870-1914 \- \- Antique Marks, accessed July 31, 2025, [https://antique-marks.com/collecting-silver-yen.html](https://antique-marks.com/collecting-silver-yen.html)  
88. Japanese yen \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Japanese\_yen](https://en.wikipedia.org/wiki/Japanese_yen)  
89. 1 yen coin \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/1\_yen\_coin](https://en.wikipedia.org/wiki/1_yen_coin)  
90. Japan Categories | NGC Registry, accessed July 31, 2025, [https://www.ngccoin.com/registry/competitive/japan/japan/](https://www.ngccoin.com/registry/competitive/japan/japan/)  
91. Japan 100 Yen Y 78 Prices & Values \- NGC, accessed July 31, 2025, [https://www.ngccoin.com/price-guide/world/japan-100-yen-y-78-yr34-cuid-54447-duid-147756](https://www.ngccoin.com/price-guide/world/japan-100-yen-y-78-yr34-cuid-54447-duid-147756)  
92. Banknotes of the Japanese yen \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Banknotes\_of\_the\_Japanese\_yen](https://en.wikipedia.org/wiki/Banknotes_of_the_Japanese_yen)  
93. JPY | Japanese Yen \- Oanda, accessed July 31, 2025, [https://www.oanda.com/currency-converter/en/currencies/majors/jpy/](https://www.oanda.com/currency-converter/en/currencies/majors/jpy/)  
94. The Japanese Dating Systems for Coinage \- PCGS, accessed July 31, 2025, [https://www.pcgs.com/news/japanese-dating-systems-for-coinage](https://www.pcgs.com/news/japanese-dating-systems-for-coinage)  
95. Reading Japanese coins \- Star City Homer collections, accessed July 31, 2025, [https://www.starcityhomer.com/reading-japanese-coins.html](https://www.starcityhomer.com/reading-japanese-coins.html)  
96. Japanese Calendar, accessed July 31, 2025, [https://www.seattle.us.emb-japan.go.jp/files/100049285.pdf](https://www.seattle.us.emb-japan.go.jp/files/100049285.pdf)  
97. Japanese economic miracle \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Japanese\_economic\_miracle](https://en.wikipedia.org/wiki/Japanese_economic_miracle)  
98. Japanese invasion money \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Japanese\_invasion\_money](https://en.wikipedia.org/wiki/Japanese_invasion_money)  
99. The Japanese Occupation Money of 1941-1945 Of Burma, Malaya, The Philippines, The Netherlands Indies, Oceania and Russia, accessed July 31, 2025, [http://asiamoney.weebly.com/japanese-occupation-money.html](http://asiamoney.weebly.com/japanese-occupation-money.html)  
100. Japanese Invasion Money Malaya 1 dollar note: Major L L Williams, 17 Battalion Volunteer Defence Corps | Australian War Memorial, accessed July 31, 2025, [https://www.awm.gov.au/collection/C1138218](https://www.awm.gov.au/collection/C1138218)  
101. en.wikipedia.org, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Korean\_Empire\_won\#:\~:text=The%20won%20was%20equivalent%20to,denominated%20in%20yen%20and%20sen.](https://en.wikipedia.org/wiki/Korean_Empire_won#:~:text=The%20won%20was%20equivalent%20to,denominated%20in%20yen%20and%20sen.)  
102. Korean Empire won \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Korean\_Empire\_won](https://en.wikipedia.org/wiki/Korean_Empire_won)  
103. Japanese government–issued dollar in Malaya and Borneo \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Japanese\_government%E2%80%93issued\_dollar\_in\_Malaya\_and\_Borneo](https://en.wikipedia.org/wiki/Japanese_government%E2%80%93issued_dollar_in_Malaya_and_Borneo)  
104. One thousand dollar note used during the Japanese Occupation \- Roots.sg, accessed July 31, 2025, [https://www.roots.gov.sg/Collection-Landing/listing/1080201](https://www.roots.gov.sg/Collection-Landing/listing/1080201)  
105. Japanese Hansatsu \- THE BANKNOTE DEN, accessed July 31, 2025, [https://banknoteden.com/collection/japan/](https://banknoteden.com/collection/japan/)  
106. Who issues Japanese banknotes? : 日本銀行 Bank of Japan, accessed July 31, 2025, [https://www.boj.or.jp/en/about/education/oshiete/money/c02.htm](https://www.boj.or.jp/en/about/education/oshiete/money/c02.htm)  
107. ISO 3166-1 alpha-2 country code: AU \- Localizely, accessed July 31, 2025, [https://localizely.com/country-code/AU/](https://localizely.com/country-code/AU/)  
108. ISO 3166-1 Country Codes, accessed July 31, 2025, [https://docs.precisely.com/docs/sftw/spectrum/22.1/en/webhelp/GlobalGeocodingGuide-REST/GlobalGeocodingGuide/source/Countries/GlobalGeocoder\_country\_codes.html](https://docs.precisely.com/docs/sftw/spectrum/22.1/en/webhelp/GlobalGeocodingGuide-REST/GlobalGeocodingGuide/source/Countries/GlobalGeocoder_country_codes.html)  
109. About Australia | Australian Government Department of Foreign ..., accessed July 31, 2025, [https://www.dfat.gov.au/about-australia](https://www.dfat.gov.au/about-australia)  
110. Tell Me About Australia \- Australian Embassy in Turkey's, accessed July 31, 2025, [https://turkey.embassy.gov.au/files/anka/TellMeAboutAustralia.pdf](https://turkey.embassy.gov.au/files/anka/TellMeAboutAustralia.pdf)  
111. Royal Australian Mint \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Royal\_Australian\_Mint](https://en.wikipedia.org/wiki/Royal_Australian_Mint)  
112. Branch Mints of the Royal Mint \- Museums Victoria Collections, accessed July 31, 2025, [https://collections.museumsvictoria.com.au/articles/3768](https://collections.museumsvictoria.com.au/articles/3768)  
113. How to identify coins made in Perth, Western Australia \- The Perth Mint, accessed July 31, 2025, [https://www.perthmint.com/news/collector/coin-collecting/western-australias-coin-minting-history-and-how-to-identify-coins-made-in-perth/](https://www.perthmint.com/news/collector/coin-collecting/western-australias-coin-minting-history-and-how-to-identify-coins-made-in-perth/)  
114. Note Printing Australia \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Note\_Printing\_Australia](https://en.wikipedia.org/wiki/Note_Printing_Australia)  
115. Note Printing Australia Ltd. \- Devex, accessed July 31, 2025, [https://www.devex.com/organizations/note-printing-australia-ltd-57667](https://www.devex.com/organizations/note-printing-australia-ltd-57667)  
116. PCGS Population Report: Australia Coins, accessed July 31, 2025, [https://www.pcgs.com/pop/australiancoins](https://www.pcgs.com/pop/australiancoins)  
117. Australia \- PCGS CoinFacts, accessed July 31, 2025, [https://www.pcgs.com/coinfacts/category/world-coins-banknotes/world-coins/australia/2540](https://www.pcgs.com/coinfacts/category/world-coins-banknotes/world-coins/australia/2540)  
118. Buy Rare Banknotes Online | Downies Collectables, accessed July 31, 2025, [https://www.downies.com/collections/rare-banknotes](https://www.downies.com/collections/rare-banknotes)  
119. Holey dollar | National Museum of Australia, accessed July 31, 2025, [https://www.nma.gov.au/explore/collection/highlights/holey-dollar](https://www.nma.gov.au/explore/collection/highlights/holey-dollar)  
120. Holey dollar \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Holey\_dollar](https://en.wikipedia.org/wiki/Holey_dollar)  
121. First Australian-made coins from government assay in Adelaide using South Australians' gold found in 1850s Victoria, accessed July 31, 2025, [https://adelaideaz.com/articles/australian-first-coins-made-at-government-assay-office-in-adelaide-using-south-australian-prospectors--gold-from-victoria](https://adelaideaz.com/articles/australian-first-coins-made-at-government-assay-office-in-adelaide-using-south-australian-prospectors--gold-from-victoria)  
122. The Adelaide Sovereign—Australia's First Gold Coin \- PCGS, accessed July 31, 2025, [https://www.pcgs.com/news/adelaide-sovereign-australias-first-gold-coin](https://www.pcgs.com/news/adelaide-sovereign-australias-first-gold-coin)  
123. ISO 3166-1 alpha-2 country code: RU \- Localizely, accessed July 31, 2025, [https://localizely.com/country-code/RU/](https://localizely.com/country-code/RU/)  
124. ISO 3166-2:RU \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/ISO\_3166-2:RU](https://en.wikipedia.org/wiki/ISO_3166-2:RU)  
125. Official Website of the Government of the Russian Federation / The ..., accessed July 31, 2025, [http://archive.government.ru/eng/gov/base/54.html](http://archive.government.ru/eng/gov/base/54.html)  
126. Russia in Facts and Numbers, accessed July 31, 2025, [https://canada.mid.ru/en/o\_rossii/russia\_in\_facts\_and\_numbers/](https://canada.mid.ru/en/o_rossii/russia_in_facts_and_numbers/)  
127. GOZNAK security papers, banknotes, coins etc. \- SARDAS Ltd.Şti., accessed July 31, 2025, [https://www.sardas.com.tr/en/goznak.html](https://www.sardas.com.tr/en/goznak.html)  
128. Goznak \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Goznak](https://en.wikipedia.org/wiki/Goznak)  
129. Moscow Mint \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Moscow\_Mint](https://en.wikipedia.org/wiki/Moscow_Mint)  
130. The birth of Russian coinage \- RareCoin, accessed July 31, 2025, [https://rarecoin.store/en/blog/the-birth-of-russian-coinage/](https://rarecoin.store/en/blog/the-birth-of-russian-coinage/)  
131. Russia (Россия, Rossiya) \- Mark Your Coin, accessed July 31, 2025, [https://markyourcoin.weebly.com/russia-105610861089108910801103-rossiya.html](https://markyourcoin.weebly.com/russia-105610861089108910801103-rossiya.html)  
132. Russian Empire \- PCGS CoinFacts, accessed July 31, 2025, [https://www.pcgs.com/coinfacts/category/world-coins/russia/russian-empire-1601-1917/5635](https://www.pcgs.com/coinfacts/category/world-coins/russia/russian-empire-1601-1917/5635)  
133. Russia Coins \- PCGS Population Report, accessed July 31, 2025, [https://www.pcgs.com/pop/russiancoins](https://www.pcgs.com/pop/russiancoins)  
134. PMG Russian Paper Money for sale | eBay, accessed July 31, 2025, [https://www.ebay.com/b/PMG-Russian-Paper-Money/3439/bn\_26653157](https://www.ebay.com/b/PMG-Russian-Paper-Money/3439/bn_26653157)  
135. PMG Banknote Russian Paper Money for sale \- eBay, accessed July 31, 2025, [https://www.ebay.com/b/PMG-Banknote-Russian-Paper-Money/3439/bn\_26653132](https://www.ebay.com/b/PMG-Banknote-Russian-Paper-Money/3439/bn_26653132)  
136. Soviet ruble \- Wikipedia, accessed July 31, 2025, [https://en.wikipedia.org/wiki/Soviet\_ruble](https://en.wikipedia.org/wiki/Soviet_ruble)  
137. Zaïre's Hyperinflation, 1990-96 \- International Monetary Fund (IMF), accessed July 31, 2025, [https://www.imf.org/external/pubs/ft/wp/wp9750.pdf](https://www.imf.org/external/pubs/ft/wp/wp9750.pdf)  
138. THE RUSSIAN CRISIS \- UNCTAD, accessed July 31, 2025, [https://unctad.org/system/files/official-document/poirrsd002.en.pdf](https://unctad.org/system/files/official-document/poirrsd002.en.pdf)  
139. Kopeck \- Catherine II \- Siberia – Numista, accessed July 31, 2025, [https://en.numista.com/catalogue/pieces17949.html](https://en.numista.com/catalogue/pieces17949.html)