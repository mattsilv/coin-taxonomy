You have selected a PhD researcher specializing in technical data validation, classification, and structured taxonomy development for this task. I am assuming this persona.To: coin-taxonomy Project ContributorFrom: Data Validation & Taxonomy SpecialistSubject: Validated & Structured Dataset: Mexican Libertad Series (Gold, Silver, Platinum)As requested, I have completed a full validation and reconciliation of the provided research materials concerning the Mexican Libertad coin series. The source data contained numerous conflicts, particularly between comprehensive reference tables 1 and individual commercial or partial sources.3The following structured data file (JSON) represents the fully validated and consolidated taxonomy.Validation & Structuring Notes:Canonical Mintage Sources: For maximum internal consistency across all denominations, the Libertad Gold Uncirculated Mintages 2022.pdf 1 and the Wikipedia Silver Uncirculated table 2 were selected as the canonical sources for all Brilliant Uncirculated (BU) mintage figures. These were the only sources that provided comprehensive data for all denominations, which is essential for a complete taxonomy. Data from conflicting sources (e.g., 1 oz Silver BU mintages from 4 or 1 oz Gold BU mintages from 3) were superseded.Special Finishes (Proof, RP, Antique): Mintage data for special finishes is not included in the main BU tables. This data was sparse and had to be manually assembled from multiple fragmented sources.5 The resulting mintage tables for these finishes are, therefore, partial and reflect only what could be validated from the provided material.Gold Fineness: A critical validation was confirming the historical fineness of the gold coins. Evidence confirms that pre-1991 gold issues (e.g., 1981, 1987) were of.900 fineness, distinct from the.999 fineness of the modern series (1991-present).2 This is explicitly noted in the data structure.Platinum Series: A 1989 Platinum 1/4 oz coin was confirmed.2 This has been included as a separate, related series for taxonomic completeness.Data Gaps: Significant data gaps persist where no information was provided, including:Technical specifications (diameter, thickness) for fractional gold coins.Comprehensive mintage tables for Silver Proof, Silver Reverse Proof, and Silver Antique finishes (only partial data was available).All mintage figures for the "Proof-like" (PL) finish, though its existence is confirmed.11The following JSON object is structured for direct import and parsing by your project.JSON{
  "libertad_taxonomy": {
    "issuer": "La Casa de Moneda de México",
    "guarantor": "Banco de México",
    "legal_tender_status": "Legal tender guaranteed by Banco de México; value based on metal content, not a fixed face value.",
    "series": {
      "gold": {
        "series_name": "Gold Libertad (Onza)",
        "denominations": {
          "1_oz": {
            "specifications": {
              "mass_g": 31.1,
              "diameter_mm": 34.5,
              "thickness_mm": 2.5
            },
            "finishes": {
              "brilliant_uncirculated": {
                "fineness_by_year": [
                  {
                    "years": "1981",
                    "fineness": ".900"
                  },
                  {
                    "years": "1991-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 1981,
                "mintage_by_year": {
                  "1981": 596000,
                  "1991": 109193,
                  "1992": 46281,
                  "1993": 73881,
                  "1994": 1000,
                  "1995": 0,
                  "1996": 0,
                  "1997": 0,
                  "1998": 0,
                  "1999": 0,
                  "2000": 2370,
                  "2001": 0,
                  "2002": 15000,
                  "2003": 500,
                  "2004": 3000,
                  "2005": 3000,
                  "2006": 4000,
                  "2007": 2500,
                  "2008": 800,
                  "2009": 6200,
                  "2010": 4000,
                  "2011": 3000,
                  "2012": 3000,
                  "2013": 2350,
                  "2014": 4050,
                  "2015": 4800,
                  "2016": 4100,
                  "2017": 900,
                  "2018": 2050,
                  "2019": 2000,
                  "2020": 1100,
                  "2021": 1050,
                  "2022": 1900
                }
              },
              "proof": {
                "fineness_by_year": [
                  {
                    "years": "1983-1989",
                    "fineness": ".900"
                  },
                  {
                    "years": "2004-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 1983,
                "mintage_by_year": {
                  "1989": 704,
                  "2004": 1800,
                  "2005": 570,
                  "2006": 520,
                  "2007": 500,
                  "2008": 500,
                  "2009": 600,
                  "2010": 600,
                  "2011": 1100,
                  "2013": 400,
                  "2014": 250,
                  "2015": 500,
                  "2016": 2100,
                  "2017": 600,
                  "2018": 1000,
                  "2019": 750,
                  "2020": 250,
                  "2021": 500,
                  "2022": 1300,
                  "2023": 1000
                }
              },
              "reverse_proof": {
                "fineness_by_year": [
                  {
                    "years": "2018-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 2018,
                "mintage_by_year": {
                  "2018": 1000,
                  "2019": 500,
                  "2020": 250,
                  "2021": 500,
                  "2022": 500,
                  "2023": 1000
                }
              }
            }
          },
          "1_2_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": null,
              "thickness_mm": null
            },
            "finishes": {
              "brilliant_uncirculated": {
                "fineness_by_year": [
                  {
                    "years": "1981",
                    "fineness": ".900"
                  },
                  {
                    "years": "1991-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 1981,
                "mintage_by_year": {
                  "1981": 193000,
                  "1991": 10000,
                  "1992": 24343,
                  "1993": 2500,
                  "1994": 2500,
                  "1995": 0,
                  "1996": 0,
                  "1997": 0,
                  "1998": 0,
                  "1999": 0,
                  "2000": 1500,
                  "2001": 0,
                  "2002": 5000,
                  "2003": 300,
                  "2004": 500,
                  "2005": 500,
                  "2006": 500,
                  "2007": 500,
                  "2008": 300,
                  "2009": 3000,
                  "2010": 1500,
                  "2011": 1500,
                  "2012": 0,
                  "2013": 500,
                  "2014": 1000,
                  "2015": 1100,
                  "2016": 1200,
                  "2017": 700,
                  "2018": 1250,
                  "2019": 1500,
                  "2020": 700,
                  "2021": 500,
                  "2022": 1000
                }
              },
              "proof": {
                "fineness_by_year": [
                  {
                    "years": "2004-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 2004,
                "mintage_by_year": {
                  "2004": 200,
                  "2005": 720,
                  "2006": 520,
                  "2007": 500,
                  "2008": 500,
                  "2009": 600,
                  "2010": 600,
                  "2011": 1100,
                  "2013": 300,
                  "2014": 250,
                  "2015": 500,
                  "2016": 2100,
                  "2017": 700,
                  "2018": 1000,
                  "2019": 650,
                  "2020": 250,
                  "2021": 450,
                  "2022": 1000,
                  "2023": 1000
                }
              },
              "reverse_proof": {
                "fineness_by_year": [
                  {
                    "years": "2018-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 2018,
                "mintage_by_year": {
                  "2018": 1000,
                  "2019": 500,
                  "2020": 250,
                  "2021": 500,
                  "2022": 500,
                  "2023": 1000
                }
              }
            }
          },
          "1_4_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": null,
              "thickness_mm": null
            },
            "finishes": {
              "brilliant_uncirculated": {
                "fineness_by_year": [
                  {
                    "years": "1981",
                    "fineness": ".900"
                  },
                  {
                    "years": "1991-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 1981,
                "mintage_by_year": {
                  "1981": 313000,
                  "1991": 10000,
                  "1992": 27321,
                  "1993": 2500,
                  "1994": 2500,
                  "1995": 0,
                  "1996": 0,
                  "1997": 0,
                  "1998": 0,
                  "1999": 0,
                  "2000": 2500,
                  "2001": 0,
                  "2002": 5000,
                  "2003": 300,
                  "2004": 1500,
                  "2005": 500,
                  "2006": 1500,
                  "2007": 500,
                  "2008": 800,
                  "2009": 3000,
                  "2010": 1500,
                  "2011": 1500,
                  "2012": 0,
                  "2013": 750,
                  "2014": 1000,
                  "2015": 1300,
                  "2016": 1000,
                  "2017": 500,
                  "2018": 1250,
                  "2019": 1500,
                  "2020": 700,
                  "2021": 500,
                  "2022": 1300
                }
              },
              "proof": {
                "fineness_by_year": [
                  {
                    "years": "1987",
                    "fineness": ".900"
                  },
                  {
                    "years": "2004-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 1987,
                "mintage_by_year": {
                  "2004": 200,
                  "2005": 3920,
                  "2006": 2120,
                  "2007": 1500,
                  "2008": 800,
                  "2009": 1700,
                  "2010": 1000,
                  "2011": 2000,
                  "2013": 600,
                  "2014": 250,
                  "2015": 500,
                  "2016": 2100,
                  "2017": 1500,
                  "2018": 1000,
                  "2019": 800,
                  "2020": 250,
                  "2021": 450,
                  "2022": 1400,
                  "2023": 1000
                }
              },
              "reverse_proof": {
                "mintage_by_year": {}
              }
            }
          },
          "1_10_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": null,
              "thickness_mm": null
            },
            "finishes": {
              "brilliant_uncirculated": {
                "fineness_by_year": [
                  {
                    "years": "1991-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 1991,
                "mintage_by_year": {
                  "1991": 10000,
                  "1992": 50592,
                  "1993": 10000,
                  "1994": 10000,
                  "1995": 0,
                  "1996": 0,
                  "1997": 0,
                  "1998": 0,
                  "1999": 0,
                  "2000": 3500,
                  "2001": 0,
                  "2002": 5000,
                  "2003": 300,
                  "2004": 2000,
                  "2005": 500,
                  "2006": 4000,
                  "2007": 1200,
                  "2008": 2500,
                  "2009": 9000,
                  "2010": 4500,
                  "2011": 6500,
                  "2012": 0,
                  "2013": 2150,
                  "2014": 2450,
                  "2015": 4100,
                  "2016": 3800,
                  "2017": 300,
                  "2018": 1500,
                  "2019": 1250,
                  "2020": 700,
                  "2021": 850,
                  "2022": 1400
                }
              },
              "proof": {
                "fineness_by_year": [
                  {
                    "years": "2004-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 2004,
                "mintage_by_year": {
                  "2004": 200,
                  "2005": 400,
                  "2006": 520,
                  "2007": 500,
                  "2008": 500,
                  "2009": 600,
                  "2010": 600,
                  "2011": 1100,
                  "2013": 300,
                  "2014": 250,
                  "2015": 500,
                  "2016": 2100,
                  "2017": 1500,
                  "2018": 1500,
                  "2019": 1000,
                  "2020": 250,
                  "2021": 450,
                  "2022": 1100,
                  "2023": 1000
                }
              },
              "reverse_proof": {
                "mintage_by_year": {}
              }
            }
          },
          "1_20_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": null,
              "thickness_mm": null
            },
            "finishes": {
              "brilliant_uncirculated": {
                "fineness_by_year": [
                  {
                    "years": "1991-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 1991,
                "mintage_by_year": {
                  "1991": 10000,
                  "1992": 63858,
                  "1993": 10000,
                  "1994": 10000,
                  "1995": 0,
                  "1996": 0,
                  "1997": 0,
                  "1998": 0,
                  "1999": 0,
                  "2000": 5300,
                  "2001": 0,
                  "2002": 5000,
                  "2003": 800,
                  "2004": 4000,
                  "2005": 3200,
                  "2006": 3000,
                  "2007": 1200,
                  "2008": 800,
                  "2009": 2000,
                  "2010": 1500,
                  "2011": 2500,
                  "2012": 0,
                  "2013": 650,
                  "2014": 1050,
                  "2015": 1300,
                  "2016": 2900,
                  "2017": 1000,
                  "2018": 2500,
                  "2019": 1500,
                  "2020": 700,
                  "2021": 1000,
                  "2022": 1100
                }
              },
              "proof": {
                "fineness_by_year": [
                  {
                    "years": "2004-present",
                    "fineness": ".999"
                  }
                ],
                "introduction_year": 2004,
                "mintage_by_year": {
                  "2004": 200,
                  "2005": 400,
                  "2006": 520,
                  "2007": 500,
                  "2008": 800,
                  "2009": 600,
                  "2010": 600,
                  "2011": 1100,
                  "2013": 300,
                  "2014": 250,
                  "2015": 500,
                  "2016": 2100,
                  "2017": 600,
                  "2018": 1000,
                  "2019": 1000,
                  "2020": 250,
                  "2021": 350,
                  "2022": 1200,
                  "2023": 1000
                }
              },
              "reverse_proof": {
                "mintage_by_year": {}
              }
            }
          }
        }
      },
      "silver": {
        "series_name": "Silver Libertad (Onza)",
        "denominations": {
          "1_kg": {
            "specifications": {
              "mass_g": 1000.0,
              "diameter_mm": 110.0,
              "thickness_mm": null,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 2008,
                "mintage_by_year": {
                  "2008": 2003,
                  "2009": 4000,
                  "2010": 5000,
                  "2011": 0,
                  "2012": 2300,
                  "2013": 0,
                  "2014": 0,
                  "2015": 2000,
                  "2016": 2000,
                  "2017": 200,
                  "2018": 500,
                  "2019": 200,
                  "2020": 500,
                  "2021": 0,
                  "2022": 200
                }
              },
              "proof": {
                "introduction_year": 2017,
                "mintage_by_year": {}
              },
              "proof_like": {
                "mintage_by_year": {}
              }
            }
          },
          "5_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": 65.0,
              "thickness_mm": null,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1996,
                "mintage_by_year": {
                  "1996": 20000,
                  "1997": 10000,
                  "1998": 3500,
                  "1999": 2800,
                  "2000": 5500,
                  "2001": 4000,
                  "2002": 8500,
                  "2003": 5000,
                  "2004": 5923,
                  "2005": 2401,
                  "2006": 3000,
                  "2007": 5000,
                  "2008": 9000,
                  "2009": 21000,
                  "2010": 9500,
                  "2011": 6000,
                  "2012": 9500,
                  "2013": 10400,
                  "2014": 6400,
                  "2015": 9500,
                  "2016": 11400,
                  "2017": 5050,
                  "2018": 16600,
                  "2019": 18000,
                  "2020": 8900,
                  "2021": 6050,
                  "2022": 7000
                }
              },
              "proof": {
                "mintage_by_year": {
                  "2016": 2750,
                  "2025": 400
                }
              },
              "reverse_proof": {
                "mintage_by_year": {
                  "2019": 1000,
                  "2020": 1000,
                  "2021": 1000,
                  "2022": 1000,
                  "2023": 1500,
                  "2024": 4000,
                  "2025": 600
                }
              },
              "proof_like": {
                "mintage_by_year": {}
              }
            }
          },
          "2_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": 48.0,
              "thickness_mm": null,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1996,
                "mintage_by_year": {
                  "1996": 50000,
                  "1997": 15000,
                  "1998": 7000,
                  "1999": 5000,
                  "2000": 9000,
                  "2001": 6700,
                  "2002": 8700,
                  "2003": 9500,
                  "2004": 11000,
                  "2005": 3549,
                  "2006": 5800,
                  "2007": 8000,
                  "2008": 17000,
                  "2009": 46000,
                  "2010": 14000,
                  "2011": 10000,
                  "2012": 18600,
                  "2013": 17400,
                  "2014": 9000,
                  "2015": 20100,
                  "2016": 17600,
                  "2017": 8900,
                  "2018": 20400,
                  "2019": 18300,
                  "2020": 5500,
                  "2021": 6500,
                  "2022": 6250
                }
              },
              "proof": {
                "mintage_by_year": {
                  "2016": 3950,
                  "2025": 300
                }
              },
              "reverse_proof": {
                "mintage_by_year": {
                  "2025": 300
                }
              },
              "proof_like": {
                "mintage_by_year": {}
              }
            }
          },
          "1_oz": {
            "specifications": {
              "mass_g": 31.103,
              "diameter_mm": 40.0,
              "thickness_mm": 3.0,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1982,
                "mintage_by_year": {
                  "1982": 1050000,
                  "1983": 1002200,
                  "1984": 1015500,
                  "1985": 2017000,
                  "1986": 1699426,
                  "1987": 500000,
                  "1988": 1000000,
                  "1989": 1396500,
                  "1990": 1200000,
                  "1991": 1650518,
                  "1992": 2458000,
                  "1993": 1000000,
                  "1994": 400000,
                  "1995": 500000,
                  "1996": 300000,
                  "1997": 100000,
                  "1998": 67000,
                  "1999": 95000,
                  "2000": 455000,
                  "2001": 385000,
                  "2002": 955000,
                  "2003": 200000,
                  "2004": 550000,
                  "2005": 600000,
                  "2006": 300000,
                  "2007": 200000,
                  "2008": 950000,
                  "2009": 1650000,
                  "2010": 1000000,
                  "2011": 1200000,
                  "2012": 746400,
                  "2013": 774100,
                  "2014": 429200,
                  "2015": 901500,
                  "2016": 1437500,
                  "2017": 636000,
                  "2018": 300000,
                  "2019": 402000,
                  "2020": 300000,
                  "2021": 450000,
                  "2022": 350000
                }
              },
              "proof": {
                "mintage_by_year": {
                  "2016": 13250,
                  "2019": 5500,
                  "2020": 5850,
                  "2021": 3450,
                  "2022": 3400,
                  "2023": 16850,
                  "2024": 18500,
                  "2025": 500
                }
              },
              "reverse_proof": {
                "introduction_year": 2015,
                "mintage_by_year": {
                  "2015": 1500,
                  "2016": 1500,
                  "2019": 1000,
                  "2020": 1000,
                  "2021": 1000,
                  "2022": 1000,
                  "2023": 1500,
                  "2024": 3000,
                  "2025": 1500
                }
              },
              "antique": {
                "introduction_year": 2018,
                "mintage_by_year": {
                  "2018": 40000,
                  "2019": 1000
                }
              },
              "proof_like": {
                "mintage_by_year": {}
              }
            }
          },
          "1_2_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": 33.0,
              "thickness_mm": null,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1991,
                "mintage_by_year": {
                  "1991": 50618,
                  "1992": 119000,
                  "1993": 90500,
                  "1994": 90100,
                  "1995": 50000,
                  "1996": 0,
                  "1997": 20000,
                  "1998": 6400,
                  "1999": 7000,
                  "2000": 20000,
                  "2001": 25000,
                  "2002": 35000,
                  "2003": 28000,
                  "2004": 20000,
                  "2005": 10000,
                  "2006": 15000,
                  "2007": 3500,
                  "2008": 9000,
                  "2009": 10000,
                  "2010": 20000,
                  "2011": 30000,
                  "2012": 17000,
                  "2013": 24500,
                  "2014": 23000,
                  "2015": 16000,
                  "2016": 30900,
                  "2017": 9050,
                  "2018": 15500,
                  "2019": 8500,
                  "2020": 7600,
                  "2021": 4500,
                  "2022": 5555
                }
              },
              "proof": {
                "mintage_by_year": {
                  "2016": 13150,
                  "2025": 200
                }
              },
              "reverse_proof": {
                "mintage_by_year": {}
              }
            }
          },
          "1_4_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": 27.0,
              "thickness_mm": null,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1991,
                "mintage_by_year": {
                  "1991": 50017,
                  "1992": 104000,
                  "1993": 90500,
                  "1994": 90100,
                  "1995": 50000,
                  "1996": 0,
                  "1997": 20000,
                  "1998": 6400,
                  "1999": 7000,
                  "2000": 21000,
                  "2001": 25000,
                  "2002": 35000,
                  "2003": 22000,
                  "2004": 15000,
                  "2005": 10000,
                  "2006": 15000,
                  "2007": 3500,
                  "2008": 9000,
                  "2009": 10000,
                  "2010": 15500,
                  "2011": 15000,
                  "2012": 16700,
                  "2013": 9600,
                  "2014": 6950,
                  "2015": 17900,
                  "2016": 17700,
                  "2017": 8100,
                  "2018": 18000,
                  "2019": 5450,
                  "2020": 4450,
                  "2021": 3250,
                  "2022": 4150
                }
              },
              "proof": {
                "mintage_by_year": {
                  "2016": 9550
                }
              },
              "reverse_proof": {
                "mintage_by_year": {}
              }
            }
          },
          "1_10_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": 20.0,
              "thickness_mm": null,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1991,
                "mintage_by_year": {
                  "1991": 50017,
                  "1992": 299933,
                  "1993": 100000,
                  "1994": 90100,
                  "1995": 50000,
                  "1996": 0,
                  "1997": 20000,
                  "1998": 6400,
                  "1999": 8000,
                  "2000": 27500,
                  "2001": 25000,
                  "2002": 35000,
                  "2003": 20000,
                  "2004": 15000,
                  "2005": 9277,
                  "2006": 15000,
                  "2007": 3500,
                  "2008": 10000,
                  "2009": 10000,
                  "2010": 12000,
                  "2011": 15000,
                  "2012": 3300,
                  "2013": 18900,
                  "2014": 6350,
                  "2015": 19900,
                  "2016": 24400,
                  "2017": 8850,
                  "2018": 20300,
                  "2019": 7200,
                  "2020": 6100,
                  "2021": 3900,
                  "2022": 4850
                }
              },
              "proof": {
                "mintage_by_year": {
                  "2016": 12650
                }
              },
              "reverse_proof": {
                "mintage_by_year": {}
              }
            }
          },
          "1_20_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": 16.0,
              "thickness_mm": null,
              "fineness": ".999"
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1991,
                "mintage_by_year": {
                  "1991": 50017,
                  "1992": 295783,
                  "1993": 100000,
                  "1994": 90100,
                  "1995": 50000,
                  "1996": 0,
                  "1997": 20000,
                  "1998": 6400,
                  "1999": 8001,
                  "2000": 57500,
                  "2001": 25000,
                  "2002": 45000,
                  "2003": 50000,
                  "2004": 30000,
                  "2005": 15000,
                  "2006": 20000,
                  "2007": 3500,
                  "2008": 7000,
                  "2009": 10000,
                  "2010": 12000,
                  "2011": 15000,
                  "2012": 0,
                  "2013": 13500,
                  "2014": 5700,
                  "2015": 18400,
                  "2016": 22900,
                  "2017": 8550,
                  "2018": 17900,
                  "2019": 7350,
                  "2020": 5450,
                  "2021": 3600,
                  "2022": 4500
                }
              },
              "proof": {
                "mintage_by_year": {
                  "2016": 12550
                }
              },
              "reverse_proof": {
                "mintage_by_year": {}
              }
            }
          }
        }
      },
      "platinum": {
        "series_name": "Platinum Libertad (Onza)",
        "denominations": {
          "1_4_oz": {
            "specifications": {
              "mass_g": null,
              "diameter_mm": null,
              "thickness_mm": null,
              "fineness": null
            },
            "finishes": {
              "brilliant_uncirculated": {
                "introduction_year": 1989,
                "mintage_by_year": {
                  "1989": 3500
                }
              }
            }
          }
        }
      }
    }
  }
}
