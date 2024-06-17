/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define SW4_29_Pin GPIO_PIN_0
#define SW4_29_GPIO_Port GPIOA
#define SW4_30_Pin GPIO_PIN_1
#define SW4_30_GPIO_Port GPIOA
#define SW4_31_Pin GPIO_PIN_2
#define SW4_31_GPIO_Port GPIOA
#define SW4_32_Pin GPIO_PIN_3
#define SW4_32_GPIO_Port GPIOA
#define SW4_28_Pin GPIO_PIN_4
#define SW4_28_GPIO_Port GPIOA
#define SW4_27_Pin GPIO_PIN_5
#define SW4_27_GPIO_Port GPIOA
#define SW4_26_Pin GPIO_PIN_6
#define SW4_26_GPIO_Port GPIOA
#define SW4_25_Pin GPIO_PIN_7
#define SW4_25_GPIO_Port GPIOA
#define SW3_21_Pin GPIO_PIN_4
#define SW3_21_GPIO_Port GPIOC
#define SW3_22_Pin GPIO_PIN_5
#define SW3_22_GPIO_Port GPIOC
#define SW3_23_Pin GPIO_PIN_1
#define SW3_23_GPIO_Port GPIOB
#define SW3_24_Pin GPIO_PIN_2
#define SW3_24_GPIO_Port GPIOB
#define SW3_20_Pin GPIO_PIN_10
#define SW3_20_GPIO_Port GPIOB
#define SW3_19_Pin GPIO_PIN_12
#define SW3_19_GPIO_Port GPIOB
#define SW3_18_Pin GPIO_PIN_13
#define SW3_18_GPIO_Port GPIOB
#define SW3_17_Pin GPIO_PIN_14
#define SW3_17_GPIO_Port GPIOB
#define SW2_13_Pin GPIO_PIN_15
#define SW2_13_GPIO_Port GPIOB
#define SW2_14_Pin GPIO_PIN_6
#define SW2_14_GPIO_Port GPIOC
#define SW2_15_Pin GPIO_PIN_7
#define SW2_15_GPIO_Port GPIOC
#define SW2_16_Pin GPIO_PIN_8
#define SW2_16_GPIO_Port GPIOC
#define SW2_12_Pin GPIO_PIN_9
#define SW2_12_GPIO_Port GPIOC
#define SW2_11_Pin GPIO_PIN_8
#define SW2_11_GPIO_Port GPIOA
#define SW2_10_Pin GPIO_PIN_9
#define SW2_10_GPIO_Port GPIOA
#define SW2_9_Pin GPIO_PIN_10
#define SW2_9_GPIO_Port GPIOA
#define SW1_6_Pin GPIO_PIN_10
#define SW1_6_GPIO_Port GPIOC
#define SW1_7_Pin GPIO_PIN_11
#define SW1_7_GPIO_Port GPIOC
#define SW1_8_Pin GPIO_PIN_12
#define SW1_8_GPIO_Port GPIOC
#define SW1_5_Pin GPIO_PIN_5
#define SW1_5_GPIO_Port GPIOB
#define SW1_4_Pin GPIO_PIN_6
#define SW1_4_GPIO_Port GPIOB
#define SW1_3_Pin GPIO_PIN_7
#define SW1_3_GPIO_Port GPIOB
#define SW1_2_Pin GPIO_PIN_8
#define SW1_2_GPIO_Port GPIOB
#define SW1_1_Pin GPIO_PIN_9
#define SW1_1_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
