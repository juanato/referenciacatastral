/*
Validar Referencia Catastral

Para el primer digito de control t�mese las 7 primeras posiciones de la referencia catastral y el numero de cargo sobre 4 posiciones justificado a la derecha (p. ej. 0027).

Para el segundo digito, t�mese la segunda parte de la referencia (posiciones 8 a 14) y las 4 posiciones del cargo.

Rempl�cese en su caso las letras por n�meros seg�n la siguiente conversi�n:

A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9, J=10, K=11, L=12, M=13, N=14, �=15, O=16, P=17, Q=18, R=19, S=20, T=21, U=22, V=23, W=24, X=25, Y=26 y Z=27

Multipliquese cada digito (o en su caso el valor correspondiente de la letra) por los siguientes valores seg�n su posici�n:

1�=13, 2�=15, 3�=12, 4�=5, 5�=4, 6�=17, 7�=9, 8�=21, 9�=3, 10�=7, 11�=1

S�mense todos los valores obtenidos y div�dase por 23, obteniendo un resto (entre 0 y 22).

Conviertase dicho resto a letra seg�n la siguiente tabla:

0 =M, 1 =Q, 2 =W, 3= E, 4 =R, 5= T, 6 =Y, 7= U, 8= I, 9= O, 10= P, 11= A, 12= S, 13= D, 14= F, 15= G, 16= H, 17= J, 18= K, 19= L, 20= B, 21= Z, 22= X
Y ya lo tenemos. Otro dia me entretendre con alguna otra curiosidad.
*/

REQUEST HB_LANG_ESWIN
REQUEST HB_CODEPAGE_ESWIN

HB_CDPSELECT('ESWIN')
HB_LANGSELECT('ESWIN')
HB_SETCODEPAGE("ESWIN")
HB_LANGSELECT( "ES" )

local cCadenaPrimerDC, cCadenaSegundoDC 
local cDevuelto := STR(ValidaRefCatUrb("2339507DG6023N0009FO") )

 

MsgInfo(cDevuelto)
return



// Sólo valida fincas urbanas
function ValidaRefCatUrb(cRefCat)
    
    local nError := 0, nValor1Dc := 0, nValor2DC := 0
    local cGrupoDC := ""
    local cLetraDc :=  'MQWERTYUIOPASDFGHJKLBZX'
    //Sólo se comprueban las referencias catastrales con 20 carácteres alfanuméricos,
	//los dos últimos corresponden a los dígitos de control.
	if empty(cRefCat) .or. len(cRefCat) != 20
    
       nError := 1 
    else

    cRefCat := UPPER(cRefCat)
    
    //SUBSTR(<cString>, <nStart>, [<nCount>]) --> cSubstring
    //Para calcular los dos dígito de control se utilizan dos subcadenas
	cCadenaPrimerDC  := UPPER( SubStr(cRefCat,1,7)  + SubStr(cRefCat, 15, 4) )
    cCadenaSegundoDC := UPPER( SubStr(cRefCat,8,7) + SubStr(cRefCat, 15, 4) )
    
    
    nValor1Dc :=  CalculaPesoPosicionCadena( cCadenaPrimerDC )
    Graba( "Valor ASCII Elemento1 DC " + STR( nValor1Dc)  ,"validador-errores.txt" )
    
    nValor2DC :=  CalculaPesoPosicionCadena( cCadenaSegundoDC )
    Graba( "Valor ASCII Elemento2 DC " + STR( nValor2Dc)  ,"validador-errores.txt" )
    
    
    cGrupoDC := SubStr( cLetraDc, nValor1Dc+1, 1 )+ SubStr( cLetraDc,nValor2Dc+1,1)
    Graba( "Producto subcadena1 " + STR( nValor1Dc) + " Producto subcadena2 " + STR(nValor2DC) + " grupo DC resultante DC " + cGrupoDC ,"validador-errores.txt" )
    //MsgInfo(cGrupoDC)    
   // MsgInfo(Acentos(cGrupoDC))
   // MsgInfo(Acentos1(cGrupoDC))
    
    
    if cGrupoDc != substr(cRefCat,19,2 )
    
        nError := 2
    else 
        nError := 0
    endif    
endif 
return (nError)


function CalculaPesoPosicionCadena( cCadena )

    local cCadenasDC, cDigitoControlCalculado
    local nAcumulaValoresPosiciones, nPesoPosicion, nPosicion

    //Valor por el que se debe multiplicar cada posición de cada subcadena
    local aPesoPosicion := {13,15,12,5,4,17,9,21,3,7,1}
    //1�=13, 2�=15, 3�=12, 4�=5, 5�=4, 6�=17, 7�=9, 8�=21, 9�=3, 10�=7, 11�=1
    
    
    local cElemento := ""




    cDigitoControlCalculado := ''
    nPesoPosicion := 0
    nPosicion := 0
    nAcumulaValoresPosiciones := 0
    FOR EACH cElemento IN cCadena
     
     
        
           
        /*
            Para el cálculo de cada dígito de control, se deben de sumar cada
            uno de los carácteres de cada cadena.
            Si el carácter no es numérico el valor corresponde de la siguiente 
            manera: A = 1, B = 2, ..., Z = 27.
        */
        cValorPosicion :=  cElemento
        nPosicion      :=  nPosicion +1

        Graba( "Cadena  "+ cCadena + " Posicion Actual "+ STR( nPosicion ) + " Elemento cadena "+ cValorPosicion ,"validador-errores.txt" )

        //A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9, J=10, K=11, L=12, M=13, N=14, �=15, O=16, P=17, Q=18, R=19, S=20, T=21, U=22, V=23, W=24, X=25, Y=26 y Z=27
           if cValorPosicion >= 'A' .and. cValorPosicion <='N'
                 nPesoPosicion := ASC( cValorPosicion ) - 64
           endif
           if  cValorPosicion =='Ñ'
                 nPesoPosicion := 15           
           endif      
               // valorCaracter=15;
           if  cValorPosicion  >'N'
               nPesoPosicion :=  ASC( cValorPosicion ) - 63
           endif   
           if cValorPosicion >= '0' .and. cValorPosicion <='9'
            nPesoPosicion := VAL( cValorPosicion ) 
           endif
      
          // nPesoPosicion := ASC( cValorPosicion )
           Graba( " Elemento cadena "+ cValorPosicion ,"validador-errores.txt" )
           Graba( " PESO POSICION      -> "  + STR( nPesoPosicion ), "validador-errores.txt" )
           Graba( " VALOR POSICION     -> "  + STR(aPesoPosicion[ nPosicion ]), "validador-errores.txt" )
           Graba( " PRODUCTO POSICION  -> "  + STR( nPesoPosicion * aPesoPosicion[ nPosicion ] ), "validador-errores.txt" )


        nAcumulaValoresPosiciones := nAcumulaValoresPosiciones + ( nPesoPosicion * aPesoPosicion[ nPosicion ] ) 
        //Valor del dígito de control calculado
        //cLetraDc.

     NEXT 
     Graba ( "ACUMULADOR PESOS DE LA CADENA " + STR(nAcumulaValoresPosiciones ), "validador-errores.txt" )
return (nAcumulaValoresPosiciones % 23)

function Graba( cTexto,cFichero )
    Local nHand, cTiempo
    cTiempo := Dtos(Date())
    cFichero :=  GetCurrentFolder()+"\"+cFichero
      
      if !File( cFichero )
         nHand := Fcreate( cFichero )
         Fwrite( nHand, cTiempo + chr(10) )
      else
         nHand := Fopen( cFichero,1 )
      endif
      Fseek( nHand,0,2 )
      Fwrite( nHand, cTexto + chr(10) )
      Fclose( nHand )
    
    return nil

