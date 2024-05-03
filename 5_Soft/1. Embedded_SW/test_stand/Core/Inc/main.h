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
#define MUX_4_E_Pin GPIO_PIN_6
#define MUX_4_E_GPIO_Port GPIOA
#define MUX_4_S0_Pin GPIO_PIN_7
#define MUX_4_S0_GPIO_Port GPIOA
#define MUX_4_S1_Pin GPIO_PIN_4
#define MUX_4_S1_GPIO_Port GPIOC
#define MUX_4_S2_Pin GPIO_PIN_5
#define MUX_4_S2_GPIO_Port GPIOC
#define MUX_3_E_Pin GPIO_PIN_0
#define MUX_3_E_GPIO_Port GPIOB
#define MUX_3_S0_Pin GPIO_PIN_1
#define MUX_3_S0_GPIO_Port GPIOB
#define MUX_3_S1_Pin GPIO_PIN_2
#define MUX_3_S1_GPIO_Port GPIOB
#define MUX_3_S2_Pin GPIO_PIN_10
#define MUX_3_S2_GPIO_Port GPIOB
#define E_U_MUX_Pin GPIO_PIN_12
#define E_U_MUX_GPIO_Port GPIOB
#define MUX_2_E_Pin GPIO_PIN_13
#define MUX_2_E_GPIO_Port GPIOB
#define MUX_2_S0_Pin GPIO_PIN_14
#define MUX_2_S0_GPIO_Port GPIOB
#define MUX_2_S1_Pin GPIO_PIN_15
#define MUX_2_S1_GPIO_Port GPIOB
#define MUX_2_S2_Pin GPIO_PIN_6
#define MUX_2_S2_GPIO_Port GPIOC
#define MUX_1_S0_Pin GPIO_PIN_8
#define MUX_1_S0_GPIO_Port GPIOC
#define MUX_1_S1_Pin GPIO_PIN_9
#define MUX_1_S1_GPIO_Port GPIOC
#define MUX_1_S2_Pin GPIO_PIN_8
#define MUX_1_S2_GPIO_Port GPIOA
#define MUX_1_E_Pin GPIO_PIN_9
#define MUX_1_E_GPIO_Port GPIOA
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
