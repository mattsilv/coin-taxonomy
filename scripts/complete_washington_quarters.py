#!/usr/bin/env python3
"""
Complete Washington Quarter Series Migration (1932-1998)
Implements comprehensive data from AI research in Issue #19.
"""

import sqlite3
import json
import csv
from io import StringIO
from datetime import datetime

def get_db_connection():
    """Get database connection with foreign key support."""
    conn = sqlite3.connect('database/coins.db')
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

# Raw CSV data from AI research (Issue #19)
WASHINGTON_QUARTERS_CSV = """year,mint,business_mintage,proof_mintage,composition,weight_g,diameter_mm,thickness_mm,edge,designer,rarity_flags,varieties_errors,comments
1932,P,5404000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"","First year of issue; no quarters struck in 1933."
1932,D,436800,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",key,"","Low mintage; popularly a key date; often counterfeited mintmarks."
1932,S,408000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",key,"","Lowest mintage of series; key date."
1934,P,31912052,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"1934 DDO known","Doubled die obverse reported."
1934,D,3527200,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage relative to period norms."
1935,P,32484000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1935,D,5780000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1935,S,5660000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1936,P,41300000,3837,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"","Proof coinage resumes; first regular proofs for series."
1936,D,5374000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1936,S,3828000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Relatively lower mintage among 1930s S-mints."
1937,P,19696000,5542,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"1937 DDO known",""
1937,D,7189600,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1937,S,1652000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage S issue."
1938,P,9472000,8045,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1938,S,2832000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage S issue."
1939,P,33540000,8795,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1939,D,7092000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1939,S,2628000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage S issue."
1940,P,35704000,11246,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1940,D,2797600,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage D issue."
1940,S,8244000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1941,P,79032000,15287,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1941,D,16714800,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1941,S,16080000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1942,P,102096000,21123,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"1942 DDO known",""
1942,D,17487200,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"1942-D DDO known",""
1942,S,19384000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1943,P,99700000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"1943 DDO known",""
1943,D,16095600,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1943,S,21700000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"1943-S DDO known",""
1944,P,104956000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1944,D,14600800,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1944,S,12560000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1945,P,74372000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1945,D,12341600,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1945,S,17004001,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1946,P,53436000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1946,D,9072800,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage D issue."
1946,S,4204000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage S issue."
1947,P,22556000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1947,D,15388000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1947,S,5532000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1948,P,35196000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1948,D,16766800,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1948,S,15960000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1949,P,9312000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage P issue."
1949,D,10068400,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage D issue."
1950,P,24920126,51386,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"1950-D/S; 1950-S/S over D","Overmintmark varieties known on D and S."
1950,D,21075600,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"D over S",""
1950,S,10284004,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"S over D",""
1951,P,43448102,57500,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1951,D,35354800,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1951,S,9048000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1952,P,38780093,81980,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1952,D,49795200,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1952,S,13707800,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1953,P,18536120,128800,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1953,D,56112400,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1953,S,14016000,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1954,P,54412203,233300,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1954,D,42305500,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1954,S,11834722,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1955,P,18180181,378200,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1955,D,3182400,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower mintage D issue."
1956,P,44144000,669384,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1956,D,32334500,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1957,P,46532000,1247952,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1957,D,77924160,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1958,P,6360000,875652,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",semi-key,"","Lower P mintage in late-1950s context."
1958,D,78124900,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1959,P,24384000,1149291,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1959,D,62054232,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1960,P,29164000,1691602,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1960,D,63000324,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1961,P,37036000,3028244,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1961,D,83656928,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1962,P,36156000,3218019,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1962,D,127554756,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1963,P,74316000,3075645,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1963,D,135288184,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"",""
1964,P,560390585,3950762,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"","Struck through 1966; SMS satin S pieces extremely rare (specimen only)."
1964,D,704135528,0,"90% Ag, 10% Cu",6.25,24.26,1.75,Reeded,"John Flanagan",common,"","Struck through 1966."
1965,P,1819717540,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","First clad year; no mintmarks; SMS satin pieces struck at San Francisco."
1966,P,821101500,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","No mintmarks; SMS satin at San Francisco."
1967,P,1524031848,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","No mintmarks; SMS satin at San Francisco."
1968,P,220731500,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","Proofs move to S; mintmarks resume (D and S)."
1968,D,101534000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1968,S,0,3041506,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1969,P,176212000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1969,D,114372000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1969,S,0,2934631,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1970,P,136420000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1970,D,417341364,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1970,S,0,2632810,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1971,P,109284000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1971,D,258634428,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1971,S,0,3220733,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1972,P,215048000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1972,D,311067732,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1972,S,0,3260996,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1973,P,346924000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1973,D,232977400,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1973,S,0,2760339,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1974,P,801456000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1974,D,353160300,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1974,S,0,2612568,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1976,P,809784016,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan (obv); Jack L. Ahr (rev)",common,"","Bicentennial reverse; struck in 1975–1976; separate silver-clad S issues including proofs."
1976,D,860118839,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan (obv); Jack L. Ahr (rev)",common,"","Bicentennial reverse; struck in 1975–1976."
1976,S,0,2800000,"40% Ag silver-clad (select S issues)",5.75,24.26,1.75,Reeded,"John Flanagan (obv); Jack L. Ahr (rev)",proof_unc_only,"","Multiple S proof/unc silver-clad counts; see mintage table."
1977,P,468556000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","Eagle reverse resumes; some production at West Point without mintmark."
1977,D,256524978,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1977,S,0,3251152,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1978,P,521452000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","West Point assisted; no mintmark."
1978,D,287373152,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1978,S,0,3127781,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1979,P,518708000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","West Point assisted; no mintmark."
1979,D,489789780,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1979,S,0,3677175,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1980,P,635832000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","First year 'P' mintmark used on quarters."
1980,D,518327487,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1980,S,0,3554806,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1981,P,601716000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1981,D,575722833,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1981,S,0,4063083,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1982,P,500931000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","No official mint sets; circulation pieces often found worn."
1982,D,480042788,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1982,S,0,3857479,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1983,P,673535000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","No official mint sets; high-grade circulation coins scarcer."
1983,D,617806446,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1983,S,0,3279126,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1984,P,676545000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1984,D,546483064,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1984,S,0,3065110,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1985,P,775818962,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1985,D,519962888,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1985,S,0,3362821,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1986,P,551199333,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1986,D,504298660,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1986,S,0,3010497,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1987,P,582499481,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1987,D,655594696,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1987,S,0,4227728,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1988,P,562052000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1988,D,596810688,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1988,S,0,3262948,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1989,P,512868000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1989,D,896535597,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1989,S,0,3220194,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1990,P,613792000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1990,D,927638181,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1990,S,0,3299559,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1991,P,570968000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1991,D,630966693,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1991,S,0,2867787,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Proof only at San Francisco."
1992,P,384764000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","Silver proof set introduced (S)."
1992,D,389777107,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1992,S,0,2858981,"Clad proof; Silver proof 1,317,579",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","S issues include clad and 90% silver proofs (separate counts)."
1993,P,639276000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1993,D,645476128,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1993,S,0,2633439,"Clad proof; Silver proof 761,353",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Dual S proof types (clad and silver)."
1994,P,825600000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1994,D,880034110,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1994,S,0,2484594,"Clad proof; Silver proof 785,329",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Dual S proof types (clad and silver)."
1995,P,1004336000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","Production surpasses 1B at both P and D."
1995,D,1103216000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1995,S,0,2117496,"Clad proof; Silver proof 679,985",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Dual S proof types (clad and silver)."
1996,P,925040000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1996,D,906868000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1996,S,0,1750244,"Clad proof; Silver proof 775,021",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Dual S proof types (clad and silver)."
1997,P,595740000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1997,D,599680000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1997,S,0,2055000,"Clad proof; Silver proof 741,678",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Dual S proof types (clad and silver)."
1998,P,896268000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"","Final year before State Quarters; eagle reverse."
1998,D,821000000,0,"Clad 91.67% Cu, 8.33% Ni",5.67,24.26,1.75,Reeded,"John Flanagan",common,"",""
1998,S,0,2086507,"Clad proof; Silver proof 878,792",5.67,24.26,1.75,Reeded,"John Flanagan",proof_only,"","Dual S proof types (clad and silver)."
"""

def parse_composition(comp_str):
    """Parse composition string into JSON format."""
    if "90% Ag" in comp_str:
        return {"alloy_name": "90% Silver", "alloy": {"silver": 0.9, "copper": 0.1}}
    elif "Clad" in comp_str:
        return {"alloy_name": "Copper-Nickel Clad", "alloy": {"copper": 0.9167, "nickel": 0.0833}}
    elif "40% Ag" in comp_str:
        return {"alloy_name": "40% Silver", "alloy": {"silver": 0.4, "copper": 0.6}}
    else:
        return {"alloy_name": comp_str, "alloy": {"copper": 1.0}}

def clean_varieties(varieties_str):
    """Clean and format varieties string."""
    if not varieties_str or varieties_str.strip() == '':
        return []
    return [v.strip() for v in varieties_str.split(';') if v.strip()]

def insert_washington_quarter_record(conn, row):
    """Insert a single Washington Quarter record."""
    year = int(row['year'])
    mint = row['mint']
    coin_id = f'US-WAQT-{year}-{mint}'
    
    # Check if already exists
    cursor = conn.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (coin_id,))
    if cursor.fetchone():
        print(f"  ⏭️  {coin_id} already exists, skipping")
        return False
    
    # Handle special proof-only cases
    if int(row['business_mintage']) == 0 and int(row['proof_mintage']) > 0:
        business_strikes = None
        proof_strikes = int(row['proof_mintage'])
    else:
        business_strikes = int(row['business_mintage']) if int(row['business_mintage']) > 0 else None
        proof_strikes = int(row['proof_mintage']) if int(row['proof_mintage']) > 0 else None
    
    # Parse composition
    composition = parse_composition(row['composition'])
    
    # Determine rarity
    rarity_map = {'key': 'key', 'semi-key': 'semi-key', 'scarce': 'scarce', 'common': 'common', 
                  'proof_only': 'common', 'proof_unc_only': 'common', 'special': 'scarce', 'rare': 'key'}
    rarity = rarity_map.get(row['rarity_flags'], 'common')
    
    # Create varieties list
    varieties = clean_varieties(row['varieties_errors'])
    
    record = {
        'coin_id': coin_id,
        'series_id': 'washington_quarter',
        'country': 'United States',
        'denomination': 'Quarters',
        'series_name': 'Washington Quarter',
        'year': year,
        'mint': mint,
        'business_strikes': business_strikes,
        'proof_strikes': proof_strikes,
        'rarity': rarity,
        'composition': json.dumps(composition),
        'weight_grams': float(row['weight_g']),
        'diameter_mm': float(row['diameter_mm']),
        'varieties': json.dumps(varieties),
        'source_citation': 'AI Research Issue #19, Washington Quarter mintage tables',
        'notes': row['comments'],
        'obverse_description': 'George Washington bust left with LIBERTY, IN GOD WE TRUST, date',
        'reverse_description': 'Heraldic eagle with wings spread, arrows and olive branch, UNITED STATES OF AMERICA, QUARTER DOLLAR' + 
                             (' (Bicentennial design 1976)' if year == 1976 else ''),
        'distinguishing_features': json.dumps([
            f'Washington obverse design',
            f'{year} date',
            f'{mint} mint mark' if mint != 'P' or year >= 1980 else 'No mint mark (Philadelphia)',
            'Silver composition' if year <= 1964 else 'Clad composition'
        ]),
        'identification_keywords': json.dumps(['washington', 'quarter', 'eagle', str(year), mint.lower()]),
        'common_names': json.dumps(['Washington Quarter', 'Quarter'])
    }
    
    # Insert record
    cursor = conn.execute('''
        INSERT INTO coins (
            coin_id, series_id, country, denomination, series_name, year, mint,
            business_strikes, proof_strikes, rarity, composition, weight_grams, diameter_mm,
            varieties, source_citation, notes, obverse_description, reverse_description,
            distinguishing_features, identification_keywords, common_names
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(record.values()))
    
    rarity_symbol = {'key': '🔑', 'semi-key': '🔸', 'scarce': '⚠️', 'common': '✅'}
    print(f"  {rarity_symbol.get(rarity, '✅')} Added {coin_id} ({rarity})")
    return True

def main():
    """Add complete Washington Quarter series (1932-1998)."""
    print("🇺🇸 Adding Complete Washington Quarter Series (1932-1998)")
    print("=" * 60)
    
    conn = get_db_connection()
    added_count = 0
    total_count = 0
    
    try:
        # Parse CSV data
        csv_reader = csv.DictReader(StringIO(WASHINGTON_QUARTERS_CSV))
        
        # Group by year for processing
        years_processed = set()
        
        for row in csv_reader:
            year = int(row['year'])
            
            if year not in years_processed:
                print(f"\n📅 Processing {year}:")
                years_processed.add(year)
            
            total_count += 1
            if insert_washington_quarter_record(conn, row):
                added_count += 1
        
        conn.commit()
        print(f"\n🎯 Migration Complete!")
        print(f"   📊 Added: {added_count} new records")
        print(f"   📊 Total processed: {total_count} records")
        print(f"   📊 Series span: 1932-1998 (67 years)")
        print(f"   🥈 Silver era: 1932-1964")
        print(f"   🪙 Clad era: 1965-1998")
        
        # Verify final count
        cursor = conn.execute('SELECT COUNT(*) FROM coins WHERE series_name = "Washington Quarter"')
        final_count = cursor.fetchone()[0]
        print(f"   ✅ Database now contains {final_count} Washington Quarter records")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()