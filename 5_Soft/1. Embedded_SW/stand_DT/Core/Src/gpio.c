/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    gpio.c
  * @brief   This file provides code for the configuration
  *          of all used GPIO pins.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "gpio.h"

/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/*----------------------------------------------------------------------------*/
/* Configure GPIO                                                             */
/*----------------------------------------------------------------------------*/
/* USER CODE BEGIN 1 */

/* USER CODE END 1 */

/** Configure pins as
        * Analog
        * Input
        * Output
        * EVENT_OUT
        * EXTI
*/
void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, SW4_29_Pin|SW4_30_Pin|SW4_31_Pin|SW4_32_Pin
                          |SW4_28_Pin|SW4_27_Pin|SW4_26_Pin|SW4_25_Pin
                          |SW2_11_Pin|SW2_10_Pin|SW2_9_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, SW3_21_Pin|SW3_22_Pin|SW2_14_Pin|SW2_15_Pin
                          |SW2_16_Pin|SW2_12_Pin|SW1_6_Pin|SW1_7_Pin
                          |SW1_8_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, SW3_23_Pin|SW3_24_Pin|SW3_20_Pin|SW3_19_Pin
                          |SW3_18_Pin|SW3_17_Pin|SW2_13_Pin|SW1_5_Pin
                          |SW1_4_Pin|SW1_3_Pin|SW1_2_Pin|SW1_1_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : PAPin PAPin PAPin PAPin
                           PAPin PAPin PAPin PAPin
                           PAPin PAPin PAPin */
  GPIO_InitStruct.Pin = SW4_29_Pin|SW4_30_Pin|SW4_31_Pin|SW4_32_Pin
                          |SW4_28_Pin|SW4_27_Pin|SW4_26_Pin|SW4_25_Pin
                          |SW2_11_Pin|SW2_10_Pin|SW2_9_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : PCPin PCPin PCPin PCPin
                           PCPin PCPin PCPin PCPin
                           PCPin */
  GPIO_InitStruct.Pin = SW3_21_Pin|SW3_22_Pin|SW2_14_Pin|SW2_15_Pin
                          |SW2_16_Pin|SW2_12_Pin|SW1_6_Pin|SW1_7_Pin
                          |SW1_8_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : PBPin PBPin PBPin PBPin
                           PBPin PBPin PBPin PBPin
                           PBPin PBPin PBPin PBPin */
  GPIO_InitStruct.Pin = SW3_23_Pin|SW3_24_Pin|SW3_20_Pin|SW3_19_Pin
                          |SW3_18_Pin|SW3_17_Pin|SW2_13_Pin|SW1_5_Pin
                          |SW1_4_Pin|SW1_3_Pin|SW1_2_Pin|SW1_1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

}

/* USER CODE BEGIN 2 */

/* USER CODE END 2 */
