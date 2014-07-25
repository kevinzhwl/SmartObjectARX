
//AcProgressBar.cpp

#include "StdAfx.h"
#include "AcProgressBar.h"
#include <rxmfcapi.h>

AcProgressBar::AcProgressBar()
{
  mIsCreated = false;
  mRangeMax = mRangeMin = mCurPos = 0;
}

AcProgressBar::~AcProgressBar()
{
  this->restore();
}

bool AcProgressBar::create(ACHAR* strHint , range_t nRangeMin, range_t nRangeMax )
{
  if (/*(nRangeMax <= 0) ||*/ (nRangeMax <= nRangeMin))
    return false;

  if(acedSetStatusBarProgressMeter(strHint , 0 , INTERNAL_RANGEMAX) != 0)
    return false;

  mIsCreated = true;
  mRangeMax = nRangeMax;
  mRangeMin = nRangeMin;

  return true;
}

void AcProgressBar::restore()
{
  if(!mIsCreated)
    return;

  acedRestoreStatusBar();
  mIsCreated = false;
  mRangeMax = mRangeMin = mCurPos = 0;
}

bool AcProgressBar::setPos(range_t nPos)
{
  if(!mIsCreated)
    return false;

  if(nPos > mRangeMax)
    nPos = mRangeMax;

  if(nPos < mRangeMin)
    nPos = mRangeMin;

  // 换算成0~INTERNAL_RANGEMAX之间的值
  int nInternalPos = double(nPos-mRangeMin)/(mRangeMax-mRangeMin)*INTERNAL_RANGEMAX;

  if (mCurPos == nInternalPos)
    return true;
  else
    mCurPos = nInternalPos;

  if(acedSetStatusBarProgressMeterPos(nInternalPos) != 0)
    return false;

  ApplicationDoEvents();
  return true;
}

bool AcProgressBar::setPos(range_t nPos,ACHAR* strHint)
{
  if(!mIsCreated)
    return false;

  if(mIsCreated)
  {
    mIsCreated = false;
    acedRestoreStatusBar();
  }

  if(acedSetStatusBarProgressMeter(strHint , mRangeMin , mRangeMax) != 0)
    return false;

  mIsCreated = true;

  if(nPos > mRangeMax)
    nPos = mRangeMax;
  if(nPos < mRangeMin)
    nPos = mRangeMin;

  // 换算成0~INTERNAL_RANGEMAX之间的值
  int nInternalPos = double(nPos-mRangeMin)/(mRangeMax-mRangeMin)*INTERNAL_RANGEMAX;

  if (mCurPos == nInternalPos)
    return true;
  else
    mCurPos = nInternalPos;

  if(acedSetStatusBarProgressMeterPos(nInternalPos) != 0)
    return false;

  ApplicationDoEvents();
  return true;
}

int AcProgressBar::ApplicationDoEvents()
{
  int res = 0;
  CWinApp *app = acedGetAcadWinApp();
  CWnd *wnd = app->GetMainWnd ();
  MSG msg;
  while (::PeekMessage (&msg, wnd->m_hWnd, 0, 0, PM_NOREMOVE))
  {
    if (!app->PumpMessage())
    {
      ::PostQuitMessage(0);
      break;
    }
  }
  LONG lIdle = 0;
  while (app->OnIdle (lIdle++));

//  res = acedUsrBrk();
//  if(res == 1 && abortString != NULL) acutPrintf(abortString);
  return res;
}

