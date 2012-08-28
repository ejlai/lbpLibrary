#ifndef __histogram_txx
#define __histogram_txx

/* ------------------------------------------------------------------------- 
  
      Program:   LBP filter for C++
      Module:    $RCSfile: histogram.txx $
      Language:  C++
      Date:      $Date: 2012-07-04 19:56:00 $
      Version:   $Revision: 0.9.0 $ 

   ------------------------------------------------------------------------- */

/* Pripojeni knihoven a hlavickovych souboru */ 
#include "histogram.h"

/* ------------------------------------------------------------------------- */

/** Funkce createSimpleHistogram(image, *histogram,  hSize) */
template <class TInputImage, class THistogramType>
  void createSimpleHistogram(typename TInputImage::Pointer image,
    typename THistogramType::ConstPointer *histogram, int hSize)
{
  // Vytvoreni adaptoru zdrojovych dat a jejich nastaveni na vstup
  typename itk::Statistics::ScalarImageToListAdaptor< TInputImage >::Pointer 
  adaptor =  itk::Statistics::ScalarImageToListAdaptor< TInputImage >::New();
  adaptor->SetImage( image );
  // Pripraveni promennych pro tvorbu histogramu
  typename itk::Statistics::ListSampleToHistogramGenerator< typename 
  itk::Statistics::ScalarImageToListAdaptor< TInputImage >, 
  typename TInputImage::PixelType >::Pointer
  generator = itk::Statistics::ListSampleToHistogramGenerator< 
  typename itk::Statistics::ScalarImageToListAdaptor< TInputImage >, 
  typename TInputImage::PixelType >::New();
  // Promenna pro uchovani velikosti histogramu 
  typename itk::Statistics::ListSampleToHistogramGenerator< 
  typename itk::Statistics::ScalarImageToListAdaptor< TInputImage >, 
  typename TInputImage::PixelType >::HistogramType::SizeType size;
  // Nastaveni sirky histogramu
  size.Fill( hSize ); 
  // Naplneni histogramu
  generator->SetListSample( adaptor );
  generator->SetNumberOfBins( size );
  generator->SetMarginalScale( 1.0 );
  generator->Update();
  *histogram = generator->GetOutput();
}

/* ------------------------------------------------------------------------- */

#endif
